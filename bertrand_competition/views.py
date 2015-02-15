# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants
from django.utils.safestring import mark_safe



def vars_for_all_templates(self):
    return {'instructions': 'bertrand_competition/Instructions.html'}


class Introduction(Page):

    template_name = 'global/Introduction.html'

    def is_displayed(self):
        return self.subsession.round_number == 1


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = ['training_my_profit']
    question = '''Suppose that you set your price at 40 points and the other\
        firm at 50 points. What would be your profit?'''

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {'question': self.question}


class Feedback1(Page):
    template_name = 'global/Feedback.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        p = self.player
        return {
            'answer': [p.training_my_profit, 40],
            'explanation': mark_safe(Question1.question + '''
                <strong>Solution: 40 points</strong>
                <strong>Explanation:</strong> Since your price was lower than\
                that of the other firm, the buyer bought from you. Hence your\
                profit would be your price, which was <strong>40\
                points</strong>.''')
        }


class Decide(Page):

    form_model = models.Player
    form_fields = ['price']


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    template_name = 'global/ResultsTable.html'

    def vars_for_template(self):
        return {
            'table': [
                ('', 'Points'),
                ('Your price', self.player.price),
                ('Lowest price', min(
                    p.price for p in self.group.get_players())),
                ('Was your product sold?',
                    'Yes' if self.player.is_a_winner else 'No'),
                ('Your profit', self.player.payoff - Constants.bonus),
                ('In addition you get a participation fee of', Constants.bonus),
                ('So in sum you will get', self.player.payoff),
            ]
        }


page_sequence = [Introduction,
            Question1,
            Feedback1,
            Decide,
            ResultsWaitPage,
            Results]
