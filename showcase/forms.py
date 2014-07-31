# -*- coding: utf-8 -*-
import showcase.models as models
from django import forms
from showcase.utilities import Form
from crispy_forms.layout import HTML


# show case forms
class DemoForm(Form):
    '''A form to showcase various form elements'''
    class Meta:
        model = models.Participant
        fields = ['demo_field1', 'demo_field2', 'demo_field3', 'demo_field4', 'demo_field5', 'demo_field6']

        widgets = {
            'demo_field1': forms.RadioSelect(),
            'demo_field2': forms.CheckboxSelectMultiple(),
            'demo_field3': forms.Textarea(),
            'demo_field4': forms.TextInput(),
            # 'demo_field5': forms.SelectMultiple(),
            'demo_field6': forms.TextInput()
        }

    def labels(self):
        return {
            'demo_field1': 'RadioButton',
            'demo_field2': 'CheckBoxes',
            'demo_field3': 'TextArea',
            'demo_field4': 'TextInput',
            'demo_field5': 'Select',
            'demo_field6': 'Numerical Input',
        }

    def demo_field6_error_message(self, value):
        '''Validating demo_field6 to allow only odd and positive numbers'''
        if value % 2 == 0 or value < 0:
            return 'The number should be odd and greater than zero'

    def order(self):
        return ['demo_field1', HTML('<p>Allows only selection of one input.</p>'),
                'demo_field2', HTML('<p>Allows for multiple selection of inputs.</p>'),
                'demo_field3', HTML('<p>Allows for entry of text input. No limit of words or characters used.</p>'),
                'demo_field4', HTML('<p>Allows for entry of text inputs, restricted to 50 letters</p>'),
                'demo_field5', HTML('<p>Allows for selection of only one input from the given list</p>'),
                'demo_field6', HTML('<p>Allows for entry of only positive odd numbers</p>'),
                ]


'''
class demoForm(Form):

    class Meta:
        model = models.Participant
        fields = ['demo_field']

    def my_field_error_message(self, value):
        if not self.treatment.your_method_here(value):
            return 'Error message goes here'

    def labels(self):
        return {}

    def initial_values(self):
        return {}

    def order(self):
        return ['demo_field', HTML('<p>demo for illustration</p>')]
'''