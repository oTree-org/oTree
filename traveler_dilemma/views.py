# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Money, money_range
from .models import Constants


def variables_for_all_templates(self):
    return dict(instructions='traveler_dilemma/Instructions.html')


class Introduction(Page):

    template_name = 'global/Introduction.html'

    def variables_for_template(self):
        return {'max_amount': Constants.max_amount,
                'min_amount': Constants.min_amount,
                'reward': Constants.reward,
                'penalty': Constants.penalty}


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = 'training_answer_mine', 'training_answer_others'
    question = '''Suppose that you claim the antiques are worth 50 points
        and the other traveler claims they are worth 100 points.
        What would you and the other traveler receive in compensation from
        the airline?'''

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        return dict(num_q=1, total_q=1, question=self.question)


class Feedback1(Page):
    template_name = 'traveler_dilemma/Feedback.html'

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        return dict(
            num_q=1, mine=self.player.training_answer_mine,
            others=self.player.training_answer_others)


class Claim(Page):

    template_name = 'traveler_dilemma/Claim.html'

    form_model = models.Player
    form_fields = ['claim']


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()


class Results(Page):

    template_name = 'global/ResultsTable.html'

    def variables_for_template(self):
        other = self.player.other_player().claim
        if self.player.claim < other:
            reward = Constants.reward
        elif self.player.claim > other:
            reward = -Constants.penalty
        else:
            reward = 0
        return dict(
            table=[
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
                ('So in sum you will get', int(self.player.payoff)),
                ])


class Question2(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = 'feedback',

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        return dict(
            num_q=1,
            title='Questionnaire',
            question='How well do you think this sample game was implemented?')


def pages():

    return [Introduction,
            Question1,
            Feedback1,
            Claim,
            ResultsWaitPage,
            Results,
            Question2]
