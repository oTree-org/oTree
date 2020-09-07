# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

class Introduction(Page):

    """Description of the game: How to play and returns expected"""
    pass

class Question(Page):

    def is_displayed(self):
        return True

    form_model = models.Player
    form_fields = ['question']


class Feedback(Page):
    def is_displayed(self):
        return True


class Contribute(Page):

    """Player: Choose how much to contribute"""

    form_model = models.Player
    form_fields = ['contribution']

    timeout_submission = {'contribution': c(Constants.endowment/2)}


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "Waiting for other participants to contribute."


class Results(Page):

    """Players payoff: How much each has earned"""

    def vars_for_template(self):

        return {
            'total_earnings': self.group.total_contribution * Constants.efficiency_factor,
            'individual_earnings': self.player.payoff - Constants.base_points,
        }

page_sequence = [Introduction,
            Question,
            Feedback,
            Contribute,
            ResultsWaitPage,
            Results]
