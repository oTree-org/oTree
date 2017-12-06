from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
In Stackelberg competition, firms decide sequentially on how many units to
produce. The unit selling price depends on the total units produced.
In this one-period implementation, the order of play is randomly determined.
"""


class Constants(BaseConstants):
    name_in_url = 'stackelberg'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'stackelberg/Instructions.html'

    # Total production capacity of both players
    total_capacity = 60

    max_units_per_player = int(total_capacity / 2)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_quantity = models.IntegerField()

    price = models.CurrencyField(
        doc="""Unit price: P = T - Q1 - Q2, where T is total capacity and Q_i are the units produced by the players"""
    )

    def set_payoffs(self):
        self.total_quantity = sum(player.quantity for player in self.get_players())
        self.price = c(Constants.total_capacity - self.total_quantity)
        for player in self.get_players():
            player.payoff = self.price * player.quantity


class Player(BasePlayer):
    quantity = models.IntegerField(
        initial=None,
        min=0, max=Constants.max_units_per_player,
        doc="""Quantity of units to produce"""
    )

    def other_player(self):
        return self.get_others_in_group()[0]
