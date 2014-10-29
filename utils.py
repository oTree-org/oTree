# -*- coding: utf-8 -*-
from __future__ import division

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
        return self.subsession.round_number ==\
            self.subsession._Constants.number_of_rounds

    def variables_for_template(self):
        ctx = {'title': 'Questionnaire',
               'note': '''Note: In this live sample game in order to save time
               for you we just put one question.'''}
        if not self.player._meta.get_field_by_name(
                'feedback')[0].verbose_name:
            ctx['question'] = '''How well do you think this sample game was
            implemented?'''
        return ctx
