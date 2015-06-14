# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>


doc = """
A demo of how rounds work in oTree, in the context of 'matching pennies'
"""

class Constants:
    name_in_url = 'matching_pennies_tutorial'
    players_per_group = 2
    num_rounds = 4
    stakes = c(100)

class Subsession(otree.models.BaseSubsession):

    def before_session_starts(self):
        if self.round_number == 1:
            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round
        if self.round_number == 3:
            # reverse the roles
            for group in self.get_groups():
                players = group.get_players()
                players.reverse()
                group.set_players(players)

class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


    def set_payoffs(self):
        matcher = self.get_player_by_role('Matcher')
        mismatcher = self.get_player_by_role('Mismatcher')

        if matcher.penny_side == mismatcher.penny_side:
            matcher.is_winner = True
            mismatcher.is_winner = False
        else:
            matcher.is_winner = False
            mismatcher.is_winner = True
        for player in [mismatcher, matcher]:
            if self.subsession.round_number == self.session.vars['paying_round'] and player.is_winner:
                player.payoff = Constants.stakes
            else:
                player.payoff = c(0)



class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    penny_side = models.CharField(
        choices=['Heads', 'Tails'],
        widget=widgets.RadioSelect()
    )

    is_winner = models.BooleanField()

    def role(self):
        if self.id_in_group == 1:
            return 'Mismatcher'
        if self.id_in_group == 2:
            return 'Matcher'

