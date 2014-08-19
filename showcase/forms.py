# -*- coding: utf-8 -*-
import showcase.models as models
from django import forms
from showcase._builtin import Form
from crispy_forms.layout import HTML


# show case forms
class DemoForm(Form):
    '''A form to showcase various form elements'''
    class Meta:
        model = models.Player
        fields = ['demo_field1', 'demo_field2', 'demo_field3', 'demo_field4', 'demo_field5']

        # custom form widgets
        widgets = {
            'demo_field1': forms.RadioSelect(),
            'demo_field2': forms.Textarea(),
            'demo_field3': forms.TextInput(),
            # 'demo_field4': forms.SelectMultiple(),
            'demo_field5': forms.TextInput()
        }

    def labels(self):
        return {
            'demo_field1': 'RadioButton',
            'demo_field2': 'TextArea',
            'demo_field3': 'TextInput',
            'demo_field4': 'Select',
            'demo_field5': 'Numerical Input',
        }

    def demo_field5_error_message(self, value):
        '''Validating demo_field6 to allow only odd and positive numbers'''
        if value % 2 == 0 or value < 0:
            return 'The number should be odd and greater than zero'

    def order(self):
        return ['demo_field1', HTML('<p>Allows only selection of one input.</p>'),
                'demo_field2', HTML('<p>Allows for entry of text input. No limit of words or characters used.</p>'),
                'demo_field3', HTML('<p>Allows for entry of text inputs, restricted to 50 letters</p>'),
                'demo_field4', HTML('<p>Allows for selection of only one input from the given select list</p>'),
                'demo_field5', HTML('<p>Allows for entry of only positive odd numbers</p>'),
                ]