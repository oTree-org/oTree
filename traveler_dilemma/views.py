# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants


def vars_for_all_templates(self):
    return {'total_q': 1, 'instructions': 'traveler_dilemma/Instructions.html'}


class Introduction(Page):

    template_name = 'global/Introduction.html'

    def vars_for_template(self):
        return {'max_amount': Constants.max_amount,
                'min_amount': Constants.min_amount,
                'reward': Constants.reward,
                'penalty': Constants.penalty}


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = ['training_answer_mine', 'training_answer_others']
    question = '''Suppose that you claim the antiques are worth 50 points and the other traveler claims they are worth 100 points. What would you and the other traveler receive in compensation from the airline?'''

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {'num_q': 1, 'question': self.question}


class Feedback(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'num_q': 1}


class Claim(Page):

    form_model = models.Player
    form_fields = ['claim']


class ResultsWaitPage(WaitPage):



    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()


class Results(Page):

    template_name = 'global/ResultsTable.html'

    def vars_for_template(self):
        other = self.player.other_player().claim
        if self.player.claim < other:
            reward = Constants.reward
        elif self.player.claim > other:
            reward = -Constants.penalty
        else:
            reward = 0
        return {
            'table': [
                ('', 'Points'),
                ('You claimed', self.player.claim),
                ('The other traveler claimed',
                 self.player.other_player().claim),
                ('Amount paid to both',
                 int(self.player.payoff - Constants.bonus - reward)),
                ('Your reward/penalty', reward and '%+i' % reward),
                ('Thus you receive',
                 int(self.player.payoff - Constants.bonus)),
                ('In addition you get a participation fee of',
                 Constants.bonus),
                ('So in sum you will get', self.player.payoff),
                ]}


page_sequence = [Introduction,
            Question1,
            Feedback,
            Claim,
            ResultsWaitPage,
            Results]
