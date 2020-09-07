# -*- coding: utf-8 -*-

import easymoney

from django.utils import translation
from django.utils.encoding import force_text

import floppyforms.__future__ as forms
import otree.db.models
import otree.forms
import otree.widgets
from .base import TestCase


class BasicWidgetTests(TestCase):

    def test_attrs_yield_form_control_class(self):
        class Form(otree.forms.Form):
            first_name = otree.forms.CharField()

        rendered = force_text(Form()['first_name'])
        elem = (
            '<input type="text" name="first_name" '
            'required class="form-control" id="id_first_name" />'
        )
        self.assertHTMLEqual(rendered, elem)


class CurrencyInputTests(TestCase):
    maxDiff = None

    class CurrencyForm(forms.Form):
        currency = otree.forms.CurrencyField()

    def test_widget(self):
        form = self.CurrencyForm({'currency': easymoney.Money('52.23')})
        rendered = force_text(form['currency'])

        self.assertTrue(
            u'''<span class="input-group-addon">€</span>''' in rendered)
        # Make sure that the value does not contain the currency symbol
        self.assertTrue('''value="52.23"''' in rendered)


class RadioSelectHorizontalTests(TestCase):
    maxDiff = None

    class RadioForm(forms.Form):
        numbers = forms.ChoiceField(choices=(
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
        ), widget=otree.forms.RadioSelectHorizontal)

    def test_widget(self):
        form = self.RadioForm()

        rendered = force_text(form['numbers'])
        self.assertHTMLEqual(
            rendered,
            """
            <label class="radio-inline" for="id_numbers_1">
                <input type="radio" id="id_numbers_1" name="numbers"
                    value="1" required /> 1
            </label>
            <label class="radio-inline" for="id_numbers_2">
                <input type="radio" id="id_numbers_2" name="numbers"
                    value="2" required /> 2
            </label>
            <label class="radio-inline" for="id_numbers_3">
                <input type="radio" id="id_numbers_3" name="numbers"
                    value="3" required /> 3
            </label>
            """)


class CheckboxInputTests(TestCase):
    maxDiff = None

    class CheckboxInputTestsModel(otree.db.models.Model):
        booleanfield = otree.db.models.BooleanField(
            widget=otree.widgets.CheckboxInput)

    def test_with_booleanfield(self):
        class Form(otree.forms.ModelForm):
            class Meta:
                model = self.CheckboxInputTestsModel
                fields = ('booleanfield',)

        form = Form(data={'booleanfield': 'on'})
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['booleanfield'] is True)

        form = Form(data={})
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['booleanfield'] is False)


class SliderInputTests(TestCase):
    maxDiff = None

    class SlideInputTestsModel(otree.db.models.Model):
        def random_invest():
            return 98

        currencyfield = otree.db.models.CurrencyField(
            min=0, max=100, default=random_invest,
            widget=otree.widgets.SliderInput())
        floatfield = otree.db.models.FloatField(
            min=0, max=2.5, default=0,
            widget=otree.widgets.SliderInput(attrs={'step': '0.01'}))

    def test_sliderinput_with_float_field(self):
        class Form(otree.forms.ModelForm):
            class Meta:
                model = self.SlideInputTestsModel
                fields = ('floatfield',)

        form = Form()
        self.assertHTMLEqual(
            force_text(form['floatfield']),
            '''
            <div class="input-group slider" data-slider>
                <input
                    type="range"
                    name="floatfield"
                    value="0"
                    required
                    max="2.5"
                    step="0.01"
                    id="id_floatfield"
                    min="0"
                    class="form-control"
                >
                <span
                    class="input-group-addon"
                    data-slider-value
                    title="current value"
                ></span>
            </div>
            ''')

    def test_sliderinput_with_float_field_and_locale_set(self):
        with translation.override('de-de'):
            self.test_sliderinput_with_float_field()

    def test_with_currencyfield(self):
        class Form(otree.forms.ModelForm):
            class Meta:
                model = self.SlideInputTestsModel
                fields = ('currencyfield',)

        form = Form()
        self.assertHTMLEqual(
            force_text(form['currencyfield']),
            '''
            <div class="input-group slider" data-slider>
                <input
                    type="range"
                    name="currencyfield"
                    value="98"
                    required
                    max="100"
                    step="0.01"
                    id="id_currencyfield"
                    min="0"
                    class="form-control"
                >
                <span
                    class="input-group-addon"
                    data-slider-value
                    title="current value"
                ></span>
            </div>
            <input
                type="hidden"
                name="initial-currencyfield"
                value="98"
                id="initial-id_currencyfield"
                class="form-control"
            >
            ''')

    def test_with_currencyfield_and_locale(self):
        with translation.override('de-de'):
            self.test_with_currencyfield()
