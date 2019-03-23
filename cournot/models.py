from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
In Cournot competition, firms simultaneously decide the units of products to
manufacture. The unit selling price depends on the total units produced. In
this implementation, there are 2 firms competing for 1 period.
"""


class Constants(BaseConstants):
    name_in_url = 'cournot'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'cournot/instructions.html'

    # Total production capacity of all players
    total_capacity = 60
    max_units_per_player = int(total_capacity / players_per_group)

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    unit_price = models.CurrencyField()

    total_units = models.IntegerField(
        doc="""Total units produced by all players"""
    )

    def set_payoffs(self):
        players = self.get_players()
        self.total_units = sum([p.units for p in players])
        self.unit_price = Constants.total_capacity - self.total_units
        for p in players:
            p.payoff = self.unit_price * p.units


class Player(BasePlayer):

    units = models.IntegerField(
        min=0, max=Constants.max_units_per_player,
        doc="""Quantity of units to produce"""
    )

    def other_player(self):
        return self.get_others_in_group()[0]


