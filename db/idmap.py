from contextlib import contextmanager
import idmap.models
import idmap.tls
import threading
import idmap

_toggle = threading.local()


def is_active():
    return getattr(_toggle, 'is_active', False)


def deactivate_cache():
    '''
    The Idmap cache is always being populated, even if it's not "active"
    We just ignore its contents.
    It doesn't look like idmap has a way to turn it off entirely.
    '''
    _toggle.is_active = False
    # 2017-08-07: flush both in activate and deactivate, just to be sure
    # i was getting some unexpected behavior in tests, when a test without
    # IDmap ran after a test with IDmap
    idmap.flush()


def activate_cache():
    idmap.flush()
    _toggle.is_active = True


@contextmanager
def use_cache():
    activate_cache()
    try:
        yield
    finally:
        deactivate_cache()


class IdMapModel(idmap.models.IdMapModel):
    class Meta:
        abstract = True
        # needs to be here for Participant and Session
        # 2018-11-24: but it seems Participant and Session don't inherit
        # from this; that's why we set use_strong_refs in the metaclass
        use_strong_refs = True

    # The ``get_cached_instance`` method is the canonical access point for
    # idmap to retrieve objects for a particular model from the cache. If it
    # returns None, then it's meant as a cache miss and the object is retrieved
    # from the database.

    # We intercept this so that we can disable the idmap cache. That is
    # required as we only want it to be active on experiment views. idmap has
    # it's problems when used together with django-channels as channels is
    # re-using threads between requests. That will result in a shared idmap
    # cache between requests, which again results in unpredictable data
    # returned from the cache as it might contain stale data.

    # The solution is to only use the cache when processing a view and clear
    # the cache before activating the use. See the activate_cache() for the
    # implementation.
    @classmethod
    def get_cached_instance(cls, *args, **kwargs):
        if is_active():
            return super().get_cached_instance(*args, **kwargs)

CLASSES_TO_SAVE = {
    'Session',
    'Participant',
    'Subsession',
    'Group',
    'Player'
}


def _get_save_objects_model_instances():
    """
    Get all model instances that should be saved. This implementation uses
    the idmap cache to determine which instances have been loaded.
    """
    # 2017-08-08: adding this because a test was failing unexpectedly for me
    # it seems reasonable that if we haven't activated the cache, we should
    # disregard it entirely.
    if not is_active():
        return []
    cache = getattr(idmap.tls._tls, 'idmap_cache', {})
    instances = []
    for model_class, model_cache in cache.items():
        # Collect instances if it's a subclass of one of the monitored
        # models.
        is_monitored = model_class.__name__ in CLASSES_TO_SAVE
        if is_monitored:
            cached_instances = list(model_cache.values())
            instances.extend(cached_instances)
    return instances


def save_objects():
    for instance in _get_save_objects_model_instances():
        # if there are no changes on the instance, SaveTheChange will detect
        # that very quickly and skip saving. I tested and it made no difference
        # if I test whether _changed_fields is empty.
        instance.save()
