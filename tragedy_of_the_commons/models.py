# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-otree-docs/wiki"""

from otree.db import models
import otree.models
from otree.common import Money, money_range

author = 'Dev'

doc = """
Tragedy of the commons.

Source code <a href="https://github.com/oTree-org/oTree/tree/master/tragedy_of_the_commons" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'tragedy_of_the_commons'


class Treatment(otree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)

    common_gain = models.MoneyField(
        doc="""""",
        default=1.00
    )
    common_loss = models.MoneyField(
        doc="""""",
        default=0.00
    )
    individual_gain = models.MoneyField(
        doc="""""",
        default=2.00
    )
    defect_costs = models.MoneyField(
        doc="""""",
        default=0.20
    )


class Match(otree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    players_per_match = 2

    def set_payoffs(self):
        if all(p.decision == 'defect' for p in self.players):
            for p in self.players:
                p.payoff = self.treatment.common_loss
        elif all(p.decision == 'cooperate' for p in self.players):
            for p in self.players:
                p.payoff = self.treatment.common_gain
        else:
            for p in self.players:
                if p.decision == 'defect':
                    p.payoff = self.treatment.individual_gain - self.treatment.defect_costs
                else:
                    p.payoff = self.treatment.common_gain - self.treatment.defect_costs


class Player(otree.models.BasePlayer):

    match = models.ForeignKey(Match, null = True)
    treatment = models.ForeignKey(Treatment, null = True)
    subsession = models.ForeignKey(Subsession)

    def other_player(self):
        """Returns other player in match. Only valid for 2-player matches."""
        return self.other_players_in_match()[0]

    decision = models.CharField(
        choices = ['cooperate', 'defect'],
        doc="""
        Players decision: cooperate or Defect
        """
    )



def treatments():
    return [Treatment.create()]