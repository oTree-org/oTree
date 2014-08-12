# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-otree-docs/wiki"""

from otree.db import models
import otree.models
from otree.common import Money, money_range

author = 'Dev'

doc = """
Tragedy of the commons.

<p>Source code <a href="https://github.com/wickens/otree_library/tree/master/tragedy_of_the_commons">here</a></p>
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

    def set_payoff(self):
        # TODO:
        # - add more players: currently 2 players
        # - modify the basic payoff logic
        if self.decision == 'defect' and self.other_player().decision == 'defect':  # all defect:
            self.payoff = self.treatment.common_loss
        elif self.decision == 'cooperate' and self.other_player().decision == 'cooperate':  # all cooperate
            self.payoff = self.treatment.common_gain
        else:  # some cooperate and others defect
            if self.decision == 'defect':
                # defector
                self.payoff = self.treatment.individual_gain - self.treatment.defect_costs
            elif self.decision == 'cooperate':
                # cooperative
                self.payoff = self.treatment.common_gain - self.treatment.defect_costs


def treatments():
    return [Treatment.create()]