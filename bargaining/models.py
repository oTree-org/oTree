# -*- coding: utf-8 -*-
from __future__ import division
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

    amount_shared = models.MoneyField(
        default=1.00,
        doc="""
        Amount to be shared by both players
        """
    )


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2

    def set_payoffs(self):
        total_requested_amount = sum([p.request_amount for p in self.players])
        if total_requested_amount < self.subsession.amount_shared:
            for p in self.players:
                p.payoff = p.request_amount
        else:
            for p in self.players:
                p.payoff = 0


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    request_amount = models.MoneyField(
        default=None,
        doc="""
        Amount requested by this player.
        """
    )

    def request_amount_choices(self):
        """Range of allowed request amount"""
        return money_range(0, self.subsession.amount_shared, 0.05)

    def other_player(self):
        """Returns the opponent of the current player"""
        return self.other_players_in_group()[0]


