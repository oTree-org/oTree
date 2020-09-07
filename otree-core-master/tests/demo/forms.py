from otree import forms
from otree import widgets
from otree.common import currency_range
from ..models import FormFieldModel


default_choices = (
    ('john', 'John'),
    ('suzanne', 'Suzanne'),
    ('one', 'One'),
    ('1', '$1.00'),
    ('2', '2'),
)


class FormFieldModelForm(forms.ModelForm):
    class Meta:
        model = FormFieldModel
        exclude = ()


class WidgetDemoForm(forms.Form):
    char = forms.CharField(required=False)

    text = forms.CharField(required=False, widget=forms.Textarea)

    radio_select = forms.ChoiceField(
        choices=default_choices,
        widget=forms.RadioSelect)
    radio_select_horizontal = forms.ChoiceField(
        choices=default_choices,
        widget=forms.RadioSelectHorizontal)

    currency = forms.CurrencyField()
    currency_choice = forms.CurrencyChoiceField(
        choices=[(m, m) for m in currency_range(0, 0.75, 0.05)]
    )

    slider = forms.IntegerField(widget=widgets.SliderInput())
    unprecise_slider = forms.IntegerField(
        widget=widgets.SliderInput(show_value=False))
    precise_slider = forms.FloatField(
        widget=widgets.SliderInput(attrs={'min': 1, 'max': 50, 'step': 0.01}))
