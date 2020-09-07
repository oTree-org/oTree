from otree_save_the_change.mixins import SaveTheChange

from otree.db import models


class SaveTheChangeFieldSupport(object):
    """
    Subclass and override methods for new fields with special behaviour.
    """

    def get_initial_value(self, instance, field, field_name):
        return self.get_value(instance, field, field_name)

    def get_value(self, instance, field, field_name):
        return getattr(instance, field_name)

    def load_value(self, field, value):
        return value

    def has_changed(self, old_value, new_value):
        return old_value != new_value


class JSONFieldSupport(SaveTheChangeFieldSupport):
    def get_value(self, instance, field, field_name):
        """
        We serialize the value into JSON. That's the value that will get
        compared to the old/new value.

        We serialize instead of making a deep copy as this will generate
        consistent results. If the JSON field contains arbitrary Python data
        that will would pickled by the JSON field, then the a deep copy will
        return dictionaries that do not equal to each other.

        Reason is that python object instances will get duplicated, and they
        might be instance that don't equal. For example::

            >>> a = object()
            >>> a == a
            True
            >>> a == copy.deepcopy(a)
            False

        Where as::

            >>> jsonfield = JSONField()
            >>> a = object()
            >>> jsonfield.get_prep_value(a) == jsonfield.get_prep_value(a)
            True
        """
        return field.get_prep_value(getattr(instance, field_name))

    def load_value(self, field, value):
        return field.to_python(value)


# To support new fields for save the change, add them here.
SAVE_THE_CHANGE_FIELD_SUPPORT = {
    models.JSONField: JSONFieldSupport(),
}


class _SaveTheChangeWithCustomFieldSupport(SaveTheChange):
    def __init__(self, *args, **kwargs):
        super(_SaveTheChangeWithCustomFieldSupport, self).__init__(
            *args, **kwargs)
        self._save_the_change_store_initial_value()

    def save(self, *args, **kwargs):
        self._save_the_change_update_changed_fields()
        return super(_SaveTheChangeWithCustomFieldSupport, self).save(
            *args, **kwargs)

    def _save_the_change_store_initial_value(self):
        self._save_the_change_initial_values = {}
        for field in self._meta.get_fields():
            if field.__class__ in SAVE_THE_CHANGE_FIELD_SUPPORT:
                field_support = SAVE_THE_CHANGE_FIELD_SUPPORT[field.__class__]
                value = field_support.get_initial_value(
                    self, field, field.name)
                self._save_the_change_initial_values[field.name] = value

    def _save_the_change_update_changed_fields(self):
        if not hasattr(self, '_changed_fields'):
            return
        initial_values = self._save_the_change_initial_values
        for field_name, old_value in initial_values.items():
            field = self._meta.get_field(field_name)
            field_support = SAVE_THE_CHANGE_FIELD_SUPPORT[field.__class__]
            new_value = field_support.get_value(self, field, field_name)
            has_changed = field_support.has_changed(old_value, new_value)
            if has_changed:
                # Trick otree_save_the_change to update custom fields.
                # Since the field might have stored an initial value that does
                # not resemble a proper field value, but a representation that
                # is easy to compare against, we need to conver the value back
                # to a proper field value that the user can work with.
                original_value = field_support.load_value(field, old_value)
                self._changed_fields[field_name] = original_value


class ModelWithVars(_SaveTheChangeWithCustomFieldSupport, models.Model):
    # don't put vars= field explicitly here, instead in subclasses,
    # for autocomplete

    class Meta:
        abstract = True
