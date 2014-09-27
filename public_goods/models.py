# -*- coding: utf-8 -*-
from otree.db import models
import otree.models
from otree.common import Money, money_range
from otree import widgets

doc = """
Public goods game. Single treatment. Four players can contribute to a joint project.
The total contribution is multiplied by some factor, the resulting amount is then divided equally between the players.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/public_goods" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'public_goods'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    endowment = models.MoneyField(
        default=3.00,
        doc="""Amount allocated to each player"""
    )

    efficiency_factor = models.FloatField(
        default=1.6,
        doc="""The multiplication factor in group contribution"""
    )


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 4

    def set_payoffs(self):
        contributions = sum([p.contribution for p in self.players])
        individual_share = contributions * self.treatment.efficiency_factor / self.players_per_match
        for p in self.players:
            p.payoff = (self.treatment.endowment - p.contribution) + individual_share


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    contribution = models.MoneyField(
        default=None,
        doc="""The amount contributed by the player""",
        widget=widgets.RangeInput(),
    )

    #def contribution_error_message(self, value):
    #    if not 0 <= value <= self.treatment.endowment:
    #        return 'Not within allowed range'

    def contribution_choices(self):
        return money_range(0, self.treatment.endowment, 0.10)



def treatments():
    return [Treatment.create()]