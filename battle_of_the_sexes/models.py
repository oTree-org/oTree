# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-otree-docs/wiki"""

from otree.db import models
import otree.models


doc = """
Battle of the sexes.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'battle_of_the_sexes'


class Treatment(otree.models.BaseTreatment):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    football_husband_amount = models.MoneyField(
        default=0.30,
        doc="""
        Amount rewarded to husband if football is chosen
        """
    )
    football_wife_amount = models.MoneyField(
        default=0.20,
        doc="""
        Amount rewarded to wife if football is chosen
        """
    )
    mismatch_amount = models.MoneyField(
        default=0.00,
        doc="""
        Amount rewarded for choosing football and opera for either players
        """
    )
    opera_husband_amount = models.MoneyField(
        default=0.20,
        doc="""
        Amount rewarded to husband if opera is chosen
        """
    )
    opera_wife_amount = models.MoneyField(
        default=0.30,
        doc="""
        Amount rewarded to wife if opera is chosen
        """
    )


class Match(otree.models.BaseMatch):
    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 2


    def set_payoffs(self):
        husband = self.get_player_by_role('husband')
        wife = self.get_player_by_role('wife')

        if husband.decision != wife.decision:
            husband.payoff = self.treatment.mismatch_amount
            wife.payoff = self.treatment.mismatch_amount

        else:
            if husband.decision == 'football':
                husband.payoff = self.treatment.football_husband_amount
                wife.payoff = self.treatment.football_wife_amount
            else:
                husband.payoff = self.treatment.opera_husband_amount
                wife.payoff = self.treatment.opera_wife_amount

class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    decision = models.CharField(
        default=None,
        choices=['football', 'opera'],
        doc='either football or opera',
    )

    def other_player(self):
        """Returns other player in match"""
        return self.other_players_in_match()[0]

    def role(self):
        if self.index_among_players_in_match == 1:
            return 'husband'
        if self.index_among_players_in_match == 2:
            return 'wife'


def treatments():
    return [Treatment.create()]