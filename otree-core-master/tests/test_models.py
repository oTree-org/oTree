from django.test import TestCase

from otree.db import models
from otree.models.varsmixin import ModelWithVars


class JSONFieldModel(ModelWithVars):
    vars = models.JSONField(default=dict)
    integer = models.IntegerField(default=0)
    json_field = models.JSONField()


class SaveTheChangeTests(TestCase):
    # We need to make sure to flash the idmap cache here after every save in
    # order to prevent getting values that do not actually represent the DB
    # values.

    def test_vars_are_saved(self):
        instance = JSONFieldModel(integer=1)
        instance.vars = {'a': 'b'}
        instance.save()

        JSONFieldModel.flush_cached_instance(instance)

        instance = JSONFieldModel.objects.get()
        self.assertEqual(instance.integer, 1)
        self.assertEqual(instance.vars, {'a': 'b'})

        instance.vars = {'c': 'd'}
        instance.save()

        JSONFieldModel.flush_cached_instance(instance)

        instance = JSONFieldModel.objects.get()
        self.assertEqual(instance.vars, {'c': 'd'})

    def test_other_json_fields_are_saved(self):
        instance = JSONFieldModel()
        instance.json_field = {'a': 'b'}
        instance.save()

        JSONFieldModel.flush_cached_instance(instance)

        instance = JSONFieldModel.objects.get()
        self.assertEqual(instance.json_field, {'a': 'b'})

        instance.integer = 2
        instance.json_field['a'] = 'd'
        instance.save()

        JSONFieldModel.flush_cached_instance(instance)

        instance = JSONFieldModel.objects.get()
        self.assertEqual(instance.integer, 2)
        self.assertEqual(instance.json_field, {'a': 'd'})
