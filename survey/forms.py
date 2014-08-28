# -*- coding: utf-8 -*-
from . import models
from django import forms
from ._builtin import Form
from otree.common import Money


class StartForm(Form):

    class Meta:
        model = models.Player
        fields = []


class DemographicsForm(Form):

    class Meta:
        model = models.Player
        fields = ['q_country',
                  'q_age',
                  'q_gender']
        widgets = {'q_gender': forms.RadioSelect()}

    def q_age_error_message(self, value):
        if not 13 <= value <= 125:
            return "Please enter a valid age"


class CognitiveReflectionTestForm(Form):

    class Meta:
        model = models.Player
        fields = ['crt_bat_float',
                  'crt_widget',
                  'crt_lake']

    def labels(self):
        return{'crt_bat_float': """A bat and a ball cost {} in total. The bat costs {} more than the ball.
                                   How much does the ball cost?""".format(Money(1.10), Money(1.00)),
               'crt_widget': """If it takes 5 machines 5 minutes to make 5 widgets,
                                how many minutes would it take 100 machines to make 100 widgets?""",
               'crt_lake': """In a lake, there is a patch of lily pads. Every day, the patch doubles in size.
                              If it takes 48 days for the patch to cover the entire lake,
                              how many days would it take for the patch to cover half of the lake?"""}
