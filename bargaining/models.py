from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
This bargaining game involves 2 players. Each demands for a portion of some
available amount. If the sum of demands is no larger than the available
amount, both players get demanded portions. Otherwise, both get nothing.
"""


class Constants(BaseConstants):
    name_in_url = 'bargaining'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'bargaining/Instructions.html'

    amount_shared = c(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    def set_payoffs(self):
        players = self.get_players()
        total_requested_amount = sum([p.request_amount for p in players])
        if total_requested_amount <= Constants.amount_shared:
            for p in players:
                p.payoff = p.request_amount
        else:
            for p in players:
                p.payoff = c(0)


class Player(BasePlayer):
    request_amount = models.CurrencyField(
        doc="""
        Amount requested by this player.
        """,
        min=0, max=Constants.amount_shared
    )

    def other_player(self):
        """Returns the opponent of the current player"""
        return self.get_others_in_group()[0]
