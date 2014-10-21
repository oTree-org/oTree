# -*- coding: utf-8 -*-
from __future__ import division
from otree import widgets
from otree.db import models

FEEDBACK_CHOICES = (
    (5, 'Very well'),
    (4, 'Well'),
    (3, 'OK'),
    (2, 'Badly'),
    (1, 'Very badly'))


class FeedbackQ(object):
    template_name = 'global/Question.html'
    form_fields = 'feedback',

    def participate_condition(self):
        return self.subsession.round_number == self.subsession.number_of_rounds

    def variables_for_template(self):
        return dict(
            title='Questionnaire',
            question='How well do you think this sample game was implemented?')
