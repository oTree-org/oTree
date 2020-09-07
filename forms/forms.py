import copy
import six
from decimal import Decimal
from six.moves import map


from django import forms
from django.forms import models as django_model_forms
from django.utils.translation import ugettext as _
from django.db.models.options import FieldDoesNotExist

import otree.common_internal
from otree.common_internal import ResponseForException
import otree.models
import otree.constants_internal
from otree.db import models
from otree.currency import Currency, RealWorldCurrency

__all__ = (
    'formfield_callback', 'modelform_factory', 'ModelForm')




def formfield_callback(db_field, **kwargs):
    # Take the `widget` attribute into account that might be set for a db
    # field.
    widget = getattr(db_field, 'widget', None)
    if widget:
        # dynamic methods like FOO_choices, FOO_min, etc
        # modify the form field's widget (self.widget)
        # Django is not designed for this kind of dynamic modification,
        # self.widget can actually be shared across
        # all instances of that form field, meaning you are modifying the
        # widget globally. However, this doesn't happen if the widget= arg
        # is a class, because then it gets instantiated, which
        # basically makes a copy.
        # i reproduced this for FOO_choices, but not for FOO_min.
        # if it's min, it sets the attrs on the widget, which means
        # a shallow copy is not enough. but until i can reproduce this,
        # leaving as is.
        if not isinstance(widget, type):
            widget = copy.copy(widget)
        kwargs['widget'] = widget
    return db_field.formfield(**kwargs)


def modelform_factory(*args, **kwargs):
    """
    2018-07-11: now this exists only to make a copy of the widget if necessary.
    maybe there is a better way.
    """
    kwargs.setdefault('formfield_callback', formfield_callback)
    return django_model_forms.modelform_factory(*args, **kwargs)

import django.forms.models

class ModelFormMetaclass(django.forms.models.ModelFormMetaclass):
    """
    Metaclass for BaseModelForm in order to inject our custom implementation of
    `formfield_callback`.
    """
    def __new__(mcs, name, bases, attrs):
        attrs.setdefault('formfield_callback', formfield_callback)
        return super(ModelFormMetaclass, mcs).__new__(
            mcs, name, bases, attrs)


class ModelForm(forms.ModelForm, metaclass=ModelFormMetaclass):
    def _get_method_from_page_or_model(self, method_name):
        for obj in [self.view, self.instance]:
            if hasattr(obj, method_name):
                meth = getattr(obj, method_name)
                if callable(meth):
                    return meth

    def __init__(self, *args, view=None, **kwargs):
        """Special handling for 'choices' argument, BooleanFields, and
        initial choice: If the user explicitly specifies a None choice
        (which is usually  rendered as '---------'), we should always respect
        it

        Otherwise:
        If the field is a BooleanField:
            if it's rendered as a Select menu (which it is by default), it
            should have a None choice
        If the field is a RadioSelect:
            it should not have a None choice
            If the DB field's value is None and the user did not specify an
            inital value, nothing should be selected by default.
            This will conceptually match a dropdown.

        """
        # first extract the view instance
        self.view = view

        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields[field_name]

            choices_method = self._get_method_from_page_or_model(f'{field_name}_choices')

            if choices_method:
                choices = choices_method()
                choices = otree.common_internal.expand_choice_tuples(choices)

                model_field = self.instance._meta.get_field(field_name)
                model_field_copy = copy.copy(model_field)

                # in Django 1.11, _choices renamed to choices
                model_field_copy.choices = choices

                field = formfield_callback(model_field_copy)
                self.fields[field_name] = field


            if isinstance(field.widget, forms.RadioSelect):
                # Fields with a RadioSelect should be rendered without the
                # '---------' option, and with nothing selected by default, to
                # match dropdowns conceptually, and because the '---------' is
                # not necessary if no item is selected initially. if the
                # selected item was the None choice, by removing it, nothing
                # is selected.

                # maybe they set the widget to Radio, but forgot to specify
                # choices. that's a mistake, but if oTree validates it, it
                # should do so somewhere else (because this is just for radio)
                # need to also check dropdown menus
                if hasattr(field, 'choices'):
                    choices = field.choices
                    if len(choices) >= 1 and choices[0][0] in {u'', None}:
                        field.choices = choices[1:]

        self._set_min_max_on_widgets()

    def _get_field_min_max(self, field_name):
        """
        Get the field boundaries from a methods defined on the view.

        Example (will get boundaries from `amount_<min|max>`):


            class Offer(Page):
                ...
                form_model = models.Group
                form_fields = ['amount']

                def amount_min(self):
                    return 1

                def amount_max(self):
                    return 5

        If the method is not found, it will return ``(None, None)``.
        """

        # SessionEditProperties is a ModelForm with extra field which is not
        # part of the model. In case your ModelForm has an extra field.
        try:
            model_field = self.instance._meta.get_field(field_name)
        except FieldDoesNotExist:
            return [None, None]

        min_method = self._get_method_from_page_or_model(f'{field_name}_min')
        if min_method:
            min_value = min_method()
        else:
            min_value = getattr(model_field, 'min', None)

        max_method = self._get_method_from_page_or_model(f'{field_name}_max')
        if max_method:
            max_value = max_method()
        else:
            max_value = getattr(model_field, 'max', None)

        return [min_value, max_value]

    def _set_min_max_on_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.NumberInput):
                min_bound, max_bound = self._get_field_min_max(field_name)
                if isinstance(min_bound, (Currency, RealWorldCurrency)):
                    min_bound = Decimal(min_bound)
                if isinstance(max_bound, (Currency, RealWorldCurrency)):
                    max_bound = Decimal(max_bound)
                if min_bound is not None:
                    field.widget.attrs['min'] = min_bound
                if max_bound is not None:
                    field.widget.attrs['max'] = max_bound
                # is this UI too intrusive?
                # if min_bound is not None and max_bound is not None:
                #    field.widget.attrs['placeholder'] = '({} - {})'.format(
                #        min_bound, max_bound
                #    )

    def boolean_field_names(self):
        boolean_fields_in_model = [
            field.name for field in self.Meta.model._meta.fields
            if isinstance(field, models.BooleanField)
        ]
        return [field_name for field_name in self.fields
                if field_name in boolean_fields_in_model]

    def _clean_fields(self):
        boolean_field_names = self.boolean_field_names()
        for name, field in self.fields.items():
            # value_from_datadict() gets the data from the data dictionaries.
            # Each widget type knows how to retrieve its own data, because some
            # widgets split data over several HTML fields.
            value = field.widget.value_from_datadict(
                self.data, self.files, self.add_prefix(name)
            )
            try:
                if isinstance(field, forms.FileField):
                    initial = self.initial.get(name, field.initial)
                    value = field.clean(value, initial)
                else:
                    value = field.clean(value)
                self.cleaned_data[name] = value

                if name in boolean_field_names and value is None:
                    mfield = self.instance._meta.get_field(name)
                    if not mfield.allow_blank:
                        msg = otree.constants_internal.field_required_msg
                        raise forms.ValidationError(msg)

                lower, upper = self._get_field_min_max(name)

                # allow blank=True and min/max to be used together
                # the field is optional, but
                # if a value is submitted, it must be within [min,max]
                if lower is None or value is None:
                    pass
                elif value < lower:
                    msg = _('Value must be greater than or equal to {}.')
                    raise forms.ValidationError(msg.format(lower))

                if upper is None or value is None:
                    pass
                elif value > upper:
                    msg = _('Value must be less than or equal to {}.')
                    raise forms.ValidationError(msg.format(upper))

                error_message_method = self._get_method_from_page_or_model(
                    f'{name}_error_message')
                if error_message_method:
                    try:
                        error_string = error_message_method(value)
                    except:
                        raise ResponseForException
                    if error_string:
                        raise forms.ValidationError(error_string)

                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value

            except forms.ValidationError as e:
                self.add_error(name, e)
        if not self.errors and hasattr(self.view, 'error_message'):
            try:
                error_string = self.view.error_message(self.cleaned_data)
            except:
                raise ResponseForException
            if error_string:
                e = forms.ValidationError(error_string)
                self.add_error(None, e)
