# -*- coding: utf-8 -*-
import demo_game.models as models
from django import forms
from demo_game._builtin import Form
from crispy_forms.layout import HTML
from django.utils.translation import ugettext


# show case forms
class DemoForm(Form):
    '''A form to demo_game various form elements'''
    class Meta:
        model = models.Player
        fields = ['demo_field1', 'demo_field2']
        # custom form widgets
        widgets = {
            'demo_field1': forms.RadioSelect(),
            'demo_field3': forms.TextInput(),
        }
    '''
    def demo_field2_error_message(self, value):
        if value != 'oTree':
            return 'The software platform name is not {}. Hint: oTree'.format(value)
    '''

    def labels(self):
        return {
            'demo_field1': '<p>Here is a radio button which is when there is only one correct answer:</p>'
                           '<p><i>I am a radio button. How many answers can you select here?</i></p>',
            'demo_field2': '<p>I am a text input field, meaning I have a restriction of characters, in this case to 5 \
            characters. For unlimited character entry one would use a text area field (these field names are Django \
            jargon by the way which is familiar to many Python programmers).</p><p><i> I am a text input field. Please enter no more than 5 letters or numbers. \
            What is the name of this software platform?</i></p>',
        }


class QuestionForm1(Form):

    class Meta:
        model = models.Player
        fields = ['training_question_1']

    def order(self):
        return [
            HTML(u'<p>{}</p>'.format(ugettext('How many understanding questions are there? \
            Please enter an odd negative number, zero or any positive number:'),)),
            'training_question_1',
        ]

    def training_question_1_error_message(self, value):
        if value < 0 and abs(value) % 2 == 0:
            return 'Please enter an odd negative number, zero or any positive number.'


class QuestionForm2(Form):

    class Meta:
        model = models.Player
        fields = ['training_question_2']
        widgets = {'training_question_2': forms.RadioSelect()}

    def order(self):
        return [
            HTML(u'<h4>{}</h4>'.format(ugettext('All the following are possible in oTree except one?'),)),
            'training_question_2',
        ]


class QuestionForm3(Form):

    class Meta:
        model = models.Player
        fields = ['training_question_3']
        widgets = {'training_question_3': forms.RadioSelect()}

    def order(self):
        return [
            HTML(u'<h4>{}</h4>'.format(ugettext('What operating system is required to use oTree?'),)),
            'training_question_3',
        ]