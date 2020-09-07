#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import six

from django.db import models
from django.db.models.fields import related
from django.core import exceptions
from django.utils.translation import ugettext_lazy
from django.apps import apps

from .serializedfields import JSONField as _JSONField
from .serializedfields import PickleField as _PickleField

import easymoney

from .idmap import SharedMemoryModelBase
from .idmap import SharedMemoryModel

import otree.common
from otree.common_internal import (
    expand_choice_tuples, get_app_label_from_import_path)
from otree.constants_internal import field_required_msg


class OTreeModelBase(SharedMemoryModelBase):

    def __new__(cls, name, bases, attrs):
        meta = attrs.get("Meta")
        module = attrs.get("__module__")
        is_concrete = not getattr(meta, "abstract", False)
        app_label = getattr(meta, "app_label", "")

        if is_concrete and module and not app_label:
            if meta is None:
                meta = type("Meta", (), {})
            app_label = get_app_label_from_import_path(module)
            meta.app_label = app_label
            meta.db_table = "{}_{}".format(app_label, name.lower())
            attrs["Meta"] = meta

        # 2015-12-22: this probably doesn't work anymore,
        # since we moved _choices to views.py
        # but we can tell users they can define FOO_choices in models.py,
        # and then call it in the equivalent method in views.py
        new_class = super(OTreeModelBase, cls).__new__(cls, name, bases, attrs)
        for f in new_class._meta.fields:
            if hasattr(new_class, f.name + '_choices'):
                attr_name = 'get_%s_display' % f.name
                setattr(new_class, attr_name, make_get_display(f))

        return new_class


def get_model(*args, **kwargs):
    return apps.get_model(*args, **kwargs)


def make_get_display(field):
    def get_FIELD_display(self):
        choices = getattr(self, field.name + '_choices')()
        value = getattr(self, field.attname)
        return dict(expand_choice_tuples(choices))[value]
    return get_FIELD_display


class OTreeModel(six.with_metaclass(OTreeModelBase, SharedMemoryModel)):
    use_strong_refs = True

    class Meta:
        abstract = True

Model = OTreeModel


class _OtreeModelFieldMixin(object):
    def fix_choices_arg(self, kwargs):
        '''allows the programmer to define choices as a list of values rather
        than (value, display_value)

        '''
        choices = kwargs.get('choices')
        if not choices:
            return
        choices = expand_choice_tuples(choices)
        kwargs['choices'] = choices

    def set_otree_properties(self, kwargs):
        self.doc = kwargs.pop('doc', None)

    def __init__(self, *args,  **kwargs):
        self.set_otree_properties(kwargs)
        self.fix_choices_arg(kwargs)

        # "initial" is an alias for default. in the context of oTree, 'initial'
        # is a more intuitive name. (since the user never instantiates objects
        # themselves. also, "default" could be misleading -- people could think
        # it's the default choice in the form
        if 'initial' in kwargs:
            kwargs.setdefault('default', kwargs.pop('initial'))

        # if default=None, Django will omit the blank choice from form widget
        # https://code.djangoproject.com/ticket/10792
        # that is contrary to the way oTree views blank/None values, so to
        # correct for this, we get rid of default=None args.
        # setting null=True already should make the field null
        if 'default' in kwargs and kwargs['default'] is None:
            kwargs.pop('default')

        super(_OtreeModelFieldMixin, self).__init__(*args, **kwargs)

    def formfield(self, *args, **kwargs):
        return super(_OtreeModelFieldMixin, self).formfield(*args, **kwargs)


class _OtreeWidgetForModelFieldMixin(object):
    """Give a `widget` argument to a model field in order to override the
    default widget used for this field in a model form.

    The given widget will only be used when you subclass your model form from
    otree.forms.forms.BaseModelForm.
    """

    def __init__(self, *args, **kwargs):
        self.widget = kwargs.pop('widget', None)
        super(_OtreeWidgetForModelFieldMixin, self).__init__(*args, **kwargs)


class _OtreeNullableModelFieldMixin(_OtreeModelFieldMixin,
                                    _OtreeWidgetForModelFieldMixin):

    def __init__(self, *args,  **kwargs):
        kwargs.setdefault('null', True)
        super(_OtreeNullableModelFieldMixin, self).__init__(*args, **kwargs)


class _OtreeNotNullableModelFieldMixin(_OtreeModelFieldMixin):
    pass


class _OtreeNumericFieldMixin(object):

    def __init__(self, *args, **kwargs):
        self.min = kwargs.pop('min', None)
        self.max = kwargs.pop('max', None)

        # 2015-2-25: deprecated, remove this
        self.bounds = kwargs.pop('bounds', None)
        super(_OtreeNumericFieldMixin, self).__init__(*args, **kwargs)

    auto_submit_default = 0


class RealWorldCurrencyField(_OtreeNullableModelFieldMixin,
                             _OtreeNumericFieldMixin, easymoney.MoneyField):

    MONEY_CLASS = otree.common.RealWorldCurrency

    auto_submit_default = otree.common.RealWorldCurrency(0)


class CurrencyField(_OtreeNullableModelFieldMixin,
                    _OtreeNumericFieldMixin, easymoney.MoneyField):

    MONEY_CLASS = otree.common.Currency

    auto_submit_default = otree.common.Currency(0)


class PickleField(_OtreeNullableModelFieldMixin, _PickleField):
    pass


class JSONField(_OtreeNullableModelFieldMixin, _JSONField):
    pass


class BooleanField(_OtreeNullableModelFieldMixin, models.NullBooleanField):
    # 2014/3/28: i just define the allowable choices on the model field,
    # instead of customizing the widget since then it works for any widget

    def __init__(self, *args,  **kwargs):
        # 2015-1-19: why is this here? isn't this the default behavior?
        # 2013-1-26: ah, because we don't want the "----" (None) choice
        if 'choices' not in kwargs:
            kwargs['choices'] = (
                (True, ugettext_lazy('Yes')),
                (False, ugettext_lazy('No'))
            )

        # We need to store whether blank is explicitly specified or not. If
        # it's not specified explicitly (which will make it default to False)
        # we need to special case validation logic in the form field if a
        # checkbox input is used.
        self._blank_is_explicit = 'blank' in kwargs

        super(BooleanField, self).__init__(*args, **kwargs)

        # you cant override "blank" or you will destroy the migration system
        self.allow_blank = bool(kwargs.get("blank"))

    auto_submit_default = False

    def clean(self, value, model_instance):
        if value is None and not self.allow_blank:
            raise exceptions.ValidationError(field_required_msg)
        return super(BooleanField, self).clean(value, model_instance)

    def formfield(self, *args, **kwargs):
        from otree import widgets

        is_checkbox_widget = isinstance(self.widget, widgets.CheckboxInput)
        if not self._blank_is_explicit and is_checkbox_widget:
            kwargs.setdefault('required', False)
        else:
            # this use the allow_blank for the form fields
            kwargs.setdefault('required', not self.allow_blank)

        return super(BooleanField, self).formfield(*args, **kwargs)


class AutoField(_OtreeNullableModelFieldMixin, models.AutoField):
    pass


class BigIntegerField(_OtreeNullableModelFieldMixin,
                      _OtreeNumericFieldMixin, models.BigIntegerField):
    auto_submit_default = 0


class BinaryField(_OtreeNullableModelFieldMixin, models.BinaryField):
    pass


# FIXME: CharField should never be nullable, otherwise we have to check for two
#        empty values: None and the empty string.
class CharField(_OtreeNullableModelFieldMixin, models.CharField):
    def __init__(self, *args,  **kwargs):
        kwargs.setdefault('max_length', 500)
        super(CharField, self).__init__(*args, **kwargs)

    auto_submit_default = ''


class CommaSeparatedIntegerField(_OtreeNullableModelFieldMixin,
                                 models.CommaSeparatedIntegerField):
    pass


class DateField(_OtreeNullableModelFieldMixin, models.DateField):
    pass


class DateTimeField(_OtreeNullableModelFieldMixin, models.DateTimeField):
    pass


class DecimalField(_OtreeNullableModelFieldMixin,
                   _OtreeNumericFieldMixin,
                   models.DecimalField):
    pass


class EmailField(_OtreeNullableModelFieldMixin, models.EmailField):
    pass


class FileField(_OtreeNullableModelFieldMixin, models.FileField):
    pass


class FilePathField(_OtreeNullableModelFieldMixin, models.FilePathField):
    pass


class FloatField(_OtreeNullableModelFieldMixin,
                 _OtreeNumericFieldMixin,
                 models.FloatField):
    pass


class IntegerField(_OtreeNullableModelFieldMixin,
                   _OtreeNumericFieldMixin, models.IntegerField):
    pass


class GenericIPAddressField(_OtreeNullableModelFieldMixin,
                            models.GenericIPAddressField):
    pass


class PositiveIntegerField(_OtreeNullableModelFieldMixin,
                           _OtreeNumericFieldMixin,
                           models.PositiveIntegerField):
    pass


class PositiveSmallIntegerField(_OtreeNullableModelFieldMixin,
                                _OtreeNumericFieldMixin,
                                models.PositiveSmallIntegerField):
    pass


class SlugField(_OtreeNullableModelFieldMixin, models.SlugField):
    pass


class SmallIntegerField(_OtreeNullableModelFieldMixin,
                        _OtreeNumericFieldMixin, models.SmallIntegerField):
    pass


class TextField(_OtreeNullableModelFieldMixin, models.TextField):
    auto_submit_default = ''


class TimeField(_OtreeNullableModelFieldMixin, models.TimeField):
    pass


class URLField(_OtreeNullableModelFieldMixin, models.URLField):
    pass


class ForeignKey(models.ForeignKey):
    pass


class ManyToOneRel(related.ManyToOneRel):
    pass


class ManyToManyField(models.ManyToManyField):
    pass


class OneToOneField(_OtreeNullableModelFieldMixin, models.OneToOneField):
    pass
