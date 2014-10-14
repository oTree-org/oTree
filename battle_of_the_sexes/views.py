# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Money, money_range
from .models import Constants

class Decide(Page):

    def participate_condition(self):
        return True

    template_name = 'battle_of_the_sexes/Decide.html'

    form_model = models.Player
    form_fields = ['decision']

    def variables_for_template(self):
        return {'role': self.player.role(),
                'fbl_husband_amt': Constants.football_husband_amount,
                'fbl_wife_amt': Constants.football_wife_amount,
                'fbl_opr_amt': Constants.mismatch_amount,
                'opr_husband_amt': Constants.opera_husband_amount,
                'opr_wife_amt': Constants.opera_wife_amount}


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def body_text(self):
        return "Waiting for the other player."


class Results(Page):

    def participate_condition(self):
        return True

    template_name = 'battle_of_the_sexes/Results.html'

    def variables_for_template(self):

        return {'other_role': self.player.other_player().role(),
                'decision': self.player.decision,
                'other_decision': self.player.other_player().decision,
                'payoff': self.player.payoff}


def pages():

    return [Decide,
            ResultsWaitPage,
            Results]
