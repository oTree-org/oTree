# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""
from otree.db import models
import otree.models
from otree.common import money_range

doc = """
The bargaining game is a two-player game used to model bargaining interactions.
Two players demand a portion of some amount of money. If the total amount
requested by the players is less than that available, both players get their request.
If their total request is greater than that available, neither player is paid.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/bargaining" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'bargaining'


class Treatment(otree.models.BaseTreatment):

    # </built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    amount_shared = models.MoneyField(
        default=1.00,
        doc="""
        Amount to be shared by both players
        """
    )


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 2

    def request_choices(self):
        """Range of allowed request amount"""
        return money_range(0, self.treatment.amount_shared, 0.05)

    def set_payoffs(self):
        total_requested_amount = sum(p.request_amount for p in self.players)
        if total_requested_amount < self.treatment.amount_shared:
            for p in self.players:
                p.payoff = p.request_amount
        else:
            for p in self.players:
                p.payoff = 0


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    request_amount = models.MoneyField(
        default=None,
        doc="""
        Amount requested by this player.
        """
    )

    def other_player(self):
        """Returns the opponent of the current player"""
        return self.other_players_in_match()[0]


def treatments():

    return [Treatment.create()]
