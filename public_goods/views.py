# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Money, money_range
from .models import Constants

def variables_for_all_templates(self):
    return {'endowment': Constants.endowment,
            'players_per_group': self.group.players_per_group,
            'efficiency_factor': Constants.efficiency_factor}


class Introduction(Page):

    """Description of the game: How to play and returns expected"""

    template_name = 'public_goods/Introduction.html'

    def variables_for_template(self):
        return {'no_of_players': self.group.players_per_group,
                'efficiency_factor': Constants.efficiency_factor}


class Question(Page):
    template_name = 'public_goods/Question.html'

    def participate_condition(self):
        return True

    form_model = models.Player
    form_fields = ['question']


class Feedback(Page):
    template_name = 'public_goods/Feedback.html'

    def participate_condition(self):
        return True

    def variables_for_template(self):
        return {'answer': self.player.question,
                'is_correct': self.player.question_correct(),
                }


class Contribute(Page):

    """Player: Choose how much to contribute"""

    form_model = models.Player
    form_fields = ['contribution']

    template_name = 'public_goods/Contribute.html'


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def body_text(self):
        return "Waiting for other participants to contribute."


class Results(Page):

    """Players payoff: How much each has earned"""

    template_name = 'public_goods/Results.html'

    def variables_for_template(self):
        # calculations here
        current_player = self.player
        other_players = self.player.get_others_in_group
        total_contribution = sum([c.contribution for c in self.group.get_players()])
        total_earnings = total_contribution * Constants.efficiency_factor
        share_earnings = total_earnings / self.group.players_per_group
        individual_earnings = (Constants.endowment - current_player.contribution) + share_earnings
        total_points = individual_earnings + Constants.base_points

        return {
            'current_player': current_player,
            'other_players': other_players,
            'total_contribution': total_contribution,
            'total_earnings': total_earnings,
            'share_earnings': share_earnings,
            'individual_earnings': individual_earnings,
            'base_points': Constants.base_points,
            'total_points': total_points
        }

class FeedbackQ(Page):
    template_name = 'public_goods/FeedbackQ.html'

    def participate_condition(self):
        return True

    form_model = models.Player
    form_fields = ['feedbackq']



def pages():

    return [Introduction,
            Question,
            Feedback,
            Contribute,
            ResultsWaitPage,
            Results,
            FeedbackQ]
