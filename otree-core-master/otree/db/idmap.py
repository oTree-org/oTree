from __future__ import absolute_import
from contextlib import contextmanager
from idmap.metaclass import SharedMemoryModelBase  # noqa
import idmap.models
import idmap.tls
import threading
from otree_save_the_change.mixins import SaveTheChange

_toggle = threading.local()


def flush_cache():
    # The cache was not initialized yet, so we don't need to clear it yet.
    if not hasattr(idmap.tls._tls, 'idmap_cache'):
        return
    for key in list(idmap.tls._tls.idmap_cache.keys()):
        del idmap.tls._tls.idmap_cache[key]


def is_active():
    return getattr(_toggle, 'is_active', False)


def deactivate_cache():
    _toggle.is_active = False


def activate_cache():
    flush_cache()
    _toggle.is_active = True


@contextmanager
def use_cache():
    activate_cache()
    try:
        yield
    finally:
        deactivate_cache()


class SharedMemoryModel(idmap.models.SharedMemoryModel):
    class Meta:
        abstract = True

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
    def get_cached_instance(cls, pk):
        if is_active():
            return idmap.tls.get_cached_instance(cls, pk)

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
    import idmap.tls
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


def _save_objects_shall_save(instance):
    # If ``SaveTheChange`` has recoreded any changes, then save.
    if isinstance(instance, SaveTheChange):
        if instance._changed_fields:
            return True
        # We need special support for the vars JSONField as SaveTheChange
        # does not detect the change.
        if hasattr(instance, '_save_the_change_update_changed_fields'):
            instance._save_the_change_update_changed_fields()
            if instance._changed_fields:
                return True
        return False
    # Save always if the model is not a SaveTheChange instance.
    return True


def save_objects():
    for instance in _get_save_objects_model_instances():
        if _save_objects_shall_save(instance):
            instance.save()
