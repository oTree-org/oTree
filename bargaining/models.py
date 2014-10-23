# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Money, money_range
import random
# </standard imports>

doc = """
This bargaining game involves 2 players. Each demands for a portion of some available amount. 
If the sum of demands is no larger than the available amount, both players get demanded portions. 
Otherwise, both get nothing.
<br />
Source code <a href="https://github.com/oTree-org/oTree/tree/master/bargaining" target="_blank">here</a>.
"""

class Constants:
    amount_shared = 100
    bonus = 10


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'bargaining'



class Group(otree.models.BaseGroup):


    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2

    def set_payoffs(self):
        players = self.get_players()
        total_requested_amount = sum([p.request_amount for p in players])
        if total_requested_amount <= Constants.amount_shared:
            for p in players:
                p.points = p.request_amount + Constants.bonus
        else:
            for p in players:
                p.points = Constants.bonus
        for p in players:
            p.payoff = 0


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    request_amount = models.PositiveIntegerField(
        doc="""
        Amount requested by this player.
        """,
        verbose_name='Please enter a number from 0 to 100'
    )
    training_amount_mine = models.PositiveIntegerField(
        verbose_name='You would get')
    training_amount_other = models.PositiveIntegerField(
        verbose_name='The other participant would get')
    points = models.PositiveIntegerField()
    feedback = models.PositiveIntegerField(
        choices=(
            (5, 'Very well'),
            (4, 'Well'),
            (3, 'OK'),
            (2, 'Badly'),
            (1, 'Very badly')), widget=widgets.RadioSelectHorizontal(),
        verbose_name='')

    def request_amount_error_message(self, value):
        if not 0 <= value <= Constants.amount_shared:
            return 'Your entry is invalid.'

    def other_player(self):
        """Returns the opponent of the current player"""
        return self.get_others_in_group()[0]
