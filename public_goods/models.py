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
This is a one-period public goods game with 3 players. Assignment to groups is random.
<br />
Source code <a href="https://github.com/oTree-org/oTree/tree/master/public_goods" target="_blank">here</a>

"""

class Constants:
    name_in_url = 'public_goods'
    players_per_group = 3
    number_of_rounds = 1

    #"""Amount allocated to each player"""
    endowment = 100
    efficiency_factor = 1.8
    base_points = 10

    question_correct = 92


class Subsession(otree.models.BaseSubsession):

    pass





class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


    def set_payoffs(self):
        contributions = sum([p.contribution for p in self.get_players()])
        individual_share = contributions * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            p.points = (Constants.endowment - p.contribution) + individual_share
            p.payoff = p.points / Constants.endowment


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    contribution = models.PositiveIntegerField(
        doc="""The amount contributed by the player""",
        widget=widgets.TextInput()
    )

    def contribution_error_message(self, value):
        if not 0 <= value <= Constants.endowment:
            return 'Your entry is invalid.'

    points = models.PositiveIntegerField()

    question = models.PositiveIntegerField(widget=widgets.TextInput())

    def question_correct(self):
        return self.question == Constants.question_correct



