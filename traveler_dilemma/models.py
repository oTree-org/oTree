# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""
from otree.db import models
import otree.models
from otree.common import money_range
from otree import forms

doc = """
Traveler's dilemma game has two players.
Each player is told to make a claim. Payoffs calculated according to the claims made.

Source code <a href="https://github.com/oTree-org/oTree/tree/master/traveler_dilemma" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'traveler_dilemma'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    reward = models.MoneyField(default=0.10,
                               doc="""Player's reward for the lowest claim""")

    penalty = models.MoneyField(default=0.10,
                                doc="""Player's deduction for the higher claim""")

    max_amount = models.MoneyField(default=1.00,
                                   doc="""The maximum claim to be requested""")
    min_amount = models.MoneyField(default=0.20,
                                   doc="""The minimum claim to be requested""")


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 2


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    # claim by player
    claim = models.MoneyField(
        default=None,
        doc="""
        Each player's claim
        """
    )

    #def claim_choices(self):
    #    """Range of allowed claim values"""
    #    return money_range(self.treatment.min_amount, self.treatment.max_amount, 0.05)

    def other_player(self):
        return self.other_players_in_match()[0]

    def set_payoff(self):
        if self.claim < self.other_player().claim:
            self.payoff = self.claim + self.treatment.reward
        elif self.claim > self.other_player().claim:
            self.payoff = self.other_player().claim - self.treatment.penalty
        else:
            self.payoff = self.claim


def treatments():

    return [Treatment.create()]
