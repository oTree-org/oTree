import floppyforms

import otree.forms
import otree.widgets
from otree.forms import ModelForm

from .base import TestCase
from .models import FormFieldModel


class TestModelForm(ModelForm):

    class Meta:
        model = FormFieldModel
        exclude = ()


class UseFloppyformWidgetsTests(TestCase):

    def test_overriden_django_fields(self):
        self.assertIsInstance(
            TestModelForm.base_fields['char'], floppyforms.CharField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['boolean'],
            floppyforms.TypedChoiceField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['big_integer'], floppyforms.IntegerField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['char'], floppyforms.CharField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['comma_separated_integer'],
            floppyforms.CharField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['date'], floppyforms.DateField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['date_time'], floppyforms.DateTimeField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['decimal'], floppyforms.DecimalField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['email'], floppyforms.EmailField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['file'], floppyforms.FileField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['file_path'],
            floppyforms.FilePathField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['float'], floppyforms.FloatField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['integer'], floppyforms.IntegerField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['generic_ip_address'],
            floppyforms.GenericIPAddressField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['positive_integer'],
            floppyforms.IntegerField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['positive_small_integer'],
            floppyforms.IntegerField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['slug'], floppyforms.SlugField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['small_integer'],
            floppyforms.IntegerField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['text'], floppyforms.CharField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['time'], floppyforms.TimeField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['url'], floppyforms.URLField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['one_to_one'],
            floppyforms.ModelChoiceField
        )

    def test_custom_fields(self):
        self.assertIsInstance(
            TestModelForm.base_fields['sent_amount'],
            otree.forms.CurrencyChoiceField
        )

    def test_currency_field(self):
        self.assertIsInstance(
            TestModelForm.base_fields['currency'],
            otree.forms.CurrencyField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['currency'].widget,
            otree.widgets.CurrencyInput
        )
        self.assertIsInstance(
            TestModelForm.base_fields['currency_choice'],
            otree.forms.CurrencyChoiceField
        )
        self.assertIsInstance(
            TestModelForm.base_fields['currency_choice'].widget,
            otree.widgets.Select
        )
