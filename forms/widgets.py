from decimal import Decimal

from django.conf import settings
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy
from otree.currency import Currency, RealWorldCurrency
from django.forms.widgets import * # noqa
from django import forms


from otree.currency.locale import CURRENCY_SYMBOLS


class _BaseMoneyInput(forms.NumberInput):
    # step = 0.01
    template_name = 'otree/forms/moneyinput.html'

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context['currency_symbol'] = self.CURRENCY_SYMBOL
        return context

    def format_value(self, value):
        if isinstance(value, (Currency, RealWorldCurrency)):
            value = Decimal(value)
        return force_text(value)


class _RealWorldCurrencyInput(_BaseMoneyInput):
    '''it's a class attribute so take care with patching it in tests'''
    CURRENCY_SYMBOL = CURRENCY_SYMBOLS.get(
        settings.REAL_WORLD_CURRENCY_CODE,
        settings.REAL_WORLD_CURRENCY_CODE,
    )


class _CurrencyInput(_RealWorldCurrencyInput):
    '''it's a class attribute so take care with patching it in tests'''
    if settings.USE_POINTS:
        if hasattr(settings, 'POINTS_CUSTOM_NAME'):
            CURRENCY_SYMBOL = settings.POINTS_CUSTOM_NAME
        else:
            # Translators: the label next to a "points" input field
            CURRENCY_SYMBOL = ugettext_lazy('points')


class RadioSelectHorizontal(forms.RadioSelect):
    template_name = 'otree/forms/radio_select_horizontal.html'


class Slider(forms.NumberInput):
    input_type = 'range'
    template_name = 'otree/forms/slider.html'
    show_value = True

    def __init__(self, *args, show_value=None, **kwargs):
        try:
            # fix bug where currency "step" values were ignored.
            step = kwargs['attrs']['step']
            kwargs['attrs']['step'] = self.format_value(step)
        except KeyError:
            pass
        if show_value is not None:
            self.show_value = show_value
        super().__init__(*args, **kwargs)

    def format_value(self, value):
        if isinstance(value, (Currency, RealWorldCurrency)):
            value = Decimal(value)
        return force_text(value)

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context['show_value'] = self.show_value
        return context

class SliderInput(Slider):
    '''old name for Slider widget'''
    pass
