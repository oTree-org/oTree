# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree import widgets
from otree.common import Currency as c, currency_range
import random

# </standard imports>


doc = """
This is the familiar playground game "Matching Pennies". In this
implementation, players are randomly grouped in the beginning and then continue
to play against the same opponent for 3 rounds. Their roles alters between
rounds.<br/>
"""


class Constants(BaseConstants):
    name_in_url = 'matching_pennies'
    players_per_group = 2
    num_rounds = 3

    instructions_template = 'matching_pennies/Instructions.html'


class Subsession(BaseSubsession):
    def before_session_starts(self):
        if self.round_number % 2 == 0:
            for group in self.get_groups():
                players = group.get_players()
                players.reverse()
                group.set_players(players)


class Group(BaseGroup):
    def set_payoffs(self):
        p1 = self.get_player_by_role('Player 1')
        p2 = self.get_player_by_role('Player 2')

        if p2.penny_side == p1.penny_side:
            p2.payoff = 100
            p1.payoff = 0
            p2.is_winner = True
            p1.is_winner = False
        else:
            p2.payoff = 0
            p1.payoff = 100
            p2.is_winner = False
            p1.is_winner = True


class Player(BasePlayer):
    penny_side = models.CharField(
        choices=['Heads', 'Tails'],
        doc="""Heads or tails""",
        widget=widgets.RadioSelect()
    )

    is_winner = models.BooleanField(
        doc="""Whether player won the round"""
    )

    def other_player(self):
        """Returns the opponent of the current player"""
        return self.get_others_in_group()[0]

    def role(self):
        if self.id_in_group == 1:
            return 'Player 1'
        if self.id_in_group == 2:
            return 'Player 2'
