# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Money, money_range
from .models import Constants

def variables_for_all_templates(self):

    return {'cooperate_amount': Constants.cooperate_amount,
            'cooperate_defect_amount': Constants.cooperate_defect_amount,
            'defect_amount': Constants.defect_amount,
            'defect_cooperate_amount': Constants.defect_cooperate_amount,
            'total_q': 1}


class Introduction(Page):

    template_name = 'prisoner/Introduction.html'


class QuestionOne(Page):

    template_name = 'prisoner/Question.html'

    form_model = models.Player
    form_fields = ['training_question_1']

    def variables_for_template(self):
        return {'num_q': 1}


class FeedbackOne(Page):

    template_name = 'prisoner/Feedback.html'

    def variables_for_template(self):
        return {'num_q': 1,
                'question': 'Suppose Alice chose to defect and Bob chose to cooperate. How many points would Alice and Bob receive, respectively?',
                'answer': self.player.training_question_1,
                'correct': Constants.training_1_correct,
                'explanation': "Alice gets 300 points, Bob gets 0 points",
                'is_correct': self.player.is_training_question_1_correct()}


class Decision(Page):

    template_name = 'prisoner/Decision.html'

    form_model = models.Player
    form_fields = ['decision']


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def body_text(self):
        return 'Waiting for the other participant to choose.'

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_points()


class Results(Page):

    template_name = 'prisoner/Results.html'

    def variables_for_template(self):


        self.player.set_payoff()

        return {'my_decision': self.player.decision.lower(),
                'other_player_decision': self.player.other_player().decision.lower(),
                'same_choice': self.player.decision == self.player.other_player().decision,
                'points_earned': self.player.points_earned,
                'base_points': Constants.base_points,
                'total_plus_base': self.player.points_earned + Constants.base_points}


def pages():

    return [Introduction,
            QuestionOne,
            FeedbackOne,
            Decision,
            ResultsWaitPage,
            Results]
