import floppyforms.__future__ as forms
from easymoney import to_dec
from . import widgets


__all__ = ('CurrencyField', 'CurrencyChoiceField', 'RealWorldCurrencyField')


class BaseCurrencyField(forms.DecimalField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', self.widget)
        super(BaseCurrencyField, self).__init__(*args, **kwargs)


class CurrencyField(BaseCurrencyField):
    widget = widgets.CurrencyInput


class RealWorldCurrencyField(BaseCurrencyField):
    widget = widgets.RealWorldCurrencyInput


class CurrencyChoiceField(forms.TypedChoiceField):
    def __init__(self, *args, **kwargs):
        super(CurrencyChoiceField, self).__init__(*args, **kwargs)
        self.choices = [(to_dec(k), v) for k, v in self.choices]

    def prepare_value(self, value):
        return to_dec(value)
