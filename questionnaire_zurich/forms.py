# -*- coding: utf-8 -*-
from . import models
from django import forms
from .utilities import ParticipantMixin
from django.utils.translation import ugettext_lazy as _
from ptree.common import currency
import ptree.forms


class StartForm(ParticipantMixin, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = []


class DemographicsForm(ParticipantMixin, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['q_country',
                  'q_age',
                  'q_gender',
                  'q_study',
                  'q_party',
                  'q_religion',
                  'q_religion_count',
                  'q_volunteer',
                  'q_donate']
        widgets = {'q_gender': forms.RadioSelect()}

    def q_age_error_message(self, value):
        if not 13 <= value <= 125:
           return _('Please enter a valid age')

    def q_religion_count_error_message(self, value):
        if not 0 <= value <= 1000:
           return _('Please enter a valid number')


class CognitiveReflectionTestNewForm(ParticipantMixin, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['crt_doctor',
                  'crt_meal_float',
                  'crt_run',
                  'crt_seen_before_new']


    def labels(self):
        return{'crt_doctor': _('A doctor gives you 3 pills, and tells you to take 1 pill every 30 minutes starting right away. '
                               'After how many mintues will you run out of pills?'),
               'crt_meal_float': unicode(_('A meal, including a beverage, costs '))
                           + currency(120) + unicode(_(' in total. The food costs 5 times as much as the beverage. How much does the food cost?')),
               'crt_run': _('A population of a town halves every month due to a plague. 1,000 people are still alive after 10 months. '
                            'After how many months were 2,000 people alive?')}


class CognitiveReflectionTestForm(ParticipantMixin, ptree.forms.Form):

    class Meta:
        model = models.Participant
        fields = ['crt_bat_float',
                  'crt_widget',
                  'crt_lake',
                  'crt_seen_before_old']

    def labels(self):
        return{'crt_bat_float': unicode(_('A bat and a ball cost ')) + currency(110) + unicode(_(' in total. The bat costs '))
                                  + currency(100) + unicode(_(' more than the ball. How much does the ball cost?')),
               'crt_widget': _('If it takes 5 machines 5 minutes to make 5 widgets, '
                               'how many minutes would it take 100 machines to make 100 widgets?'),
               'crt_lake': _('In a lake, there is a patch of lily pads. Every day, the patch doubles in size. '
                             'If it takes 48 days for the patch to cover the entire lake, '
                             'how many days would it take for the patch to cover half of the lake?')}
