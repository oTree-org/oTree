from decimal import Decimal

from babel.core import Locale
from django.conf import settings
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy
import babel
import babel.numbers
import easymoney
import floppyforms.__future__ as forms
import floppyforms.widgets


__all__ = (
    'BaseMoneyInput', 'CheckboxInput',
    'ClearableFileInput', 'ColorInput',
    'CurrencyInput', 'DateInput', 'DateTimeInput', 'EmailInput', 'FileInput',
    'HiddenInput', 'IPAddressInput', 'Input', 'RealWorldCurrencyInput',
    'NullBooleanSelect', 'NumberInput', 'PasswordInput',
    'PhoneNumberInput', 'RadioSelect', 'RadioSelectHorizontal', 'RangeInput',
    'SearchInput', 'Select', 'SelectDateWidget',
    'SliderInput', 'SlugInput', 'SplitDateTimeWidget',
    'SplitHiddenDateTimeWidget', 'TextInput', 'Textarea', 'TimeInput',
    'URLInput', 'Widget',
)


Widget = floppyforms.widgets.Widget
Input = floppyforms.widgets.Input
TextInput = floppyforms.widgets.TextInput
PasswordInput = floppyforms.widgets.PasswordInput
HiddenInput = floppyforms.widgets.HiddenInput
SlugInput = floppyforms.widgets.SlugInput
IPAddressInput = floppyforms.widgets.IPAddressInput
FileInput = floppyforms.widgets.FileInput
ClearableFileInput = floppyforms.widgets.ClearableFileInput
Textarea = floppyforms.widgets.Textarea
DateInput = floppyforms.widgets.DateInput
DateTimeInput = floppyforms.widgets.DateTimeInput
TimeInput = floppyforms.widgets.TimeInput
SearchInput = floppyforms.widgets.SearchInput
EmailInput = floppyforms.widgets.EmailInput
URLInput = floppyforms.widgets.URLInput
ColorInput = floppyforms.widgets.ColorInput
NumberInput = floppyforms.widgets.NumberInput
RangeInput = floppyforms.widgets.RangeInput
PhoneNumberInput = floppyforms.widgets.PhoneNumberInput
CheckboxInput = floppyforms.widgets.CheckboxInput
Select = floppyforms.widgets.Select
NullBooleanSelect = floppyforms.widgets.NullBooleanSelect
RadioSelect = floppyforms.widgets.RadioSelect
SplitDateTimeWidget = floppyforms.widgets.SplitDateTimeWidget
SplitHiddenDateTimeWidget = floppyforms.widgets.SplitHiddenDateTimeWidget
SelectDateWidget = floppyforms.widgets.SelectDateWidget

# don't use Multiple widgets because they don't correspond to any model field
# CheckboxSelectMultiple = floppyforms.widgets.CheckboxSelectMultiple
# MultiWidget = floppyforms.widgets.MultiWidget
# SelectMultiple = floppyforms.widgets.SelectMultiple
# MultipleHiddenInput = floppyforms.widgets.MultipleHiddenInput
# class CheckboxSelectMultipleHorizontal(forms.CheckboxSelectMultiple):
#    template_name = 'floppyforms/checkbox_select_horizontal.html'


class BaseMoneyInput(forms.NumberInput):
    # step = 0.01
    template_name = 'floppyforms/moneyinput.html'

    def get_context(self, *args, **kwargs):
        context = super(BaseMoneyInput, self).get_context(*args, **kwargs)
        context['currency_symbol'] = self.CURRENCY_SYMBOL
        context['currency_symbol_is_prefix'] = self.currency_symbol_is_prefix
        return context

    if settings.USE_POINTS:
        currency_symbol_is_prefix = False
    else:
        locale = Locale.parse(settings.REAL_WORLD_CURRENCY_LOCALE)
        pattern = locale.currency_formats['standard']
        currency_symbol_is_prefix = u'\xa4' in pattern.prefix[0]

    def _format_value(self, value):
        if isinstance(value, easymoney.Money):
            value = Decimal(value)
        return force_text(value)


class RealWorldCurrencyInput(BaseMoneyInput):
    CURRENCY_SYMBOL = babel.numbers.get_currency_symbol(
        settings.REAL_WORLD_CURRENCY_CODE,
        settings.REAL_WORLD_CURRENCY_LOCALE
    )


class CurrencyInput(RealWorldCurrencyInput):
    if settings.USE_POINTS:
        if hasattr(settings, 'POINTS_CUSTOM_NAME'):
            CURRENCY_SYMBOL = settings.POINTS_CUSTOM_NAME
        else:
            # Translators: the label next to a "points" input field
            CURRENCY_SYMBOL = ugettext_lazy('points')


class RadioSelectHorizontal(forms.RadioSelect):
    template_name = 'floppyforms/radio_select_horizontal.html'


class SliderInput(forms.RangeInput):
    template_name = 'floppyforms/slider.html'
    show_value = True

    def __init__(self, *args, **kwargs):
        show_value = kwargs.pop('show_value', None)
        if show_value is not None:
            self.show_value = show_value
        super(SliderInput, self).__init__(*args, **kwargs)

    def _format_value(self, value):
        if isinstance(value, easymoney.Money):
            value = Decimal(value)
        return force_text(value)

    def get_context(self, *args, **kwargs):
        context = super(SliderInput, self).get_context(*args, **kwargs)
        context['show_value'] = self.show_value
        return context
