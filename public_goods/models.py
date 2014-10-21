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
The game is preceded by one understanding question (in a real experiment you would often have more).
<br />
Source code <a href="https://github.com/oTree-org/oTree/tree/master/public_goods" target="_blank">here</a>

"""

class Constants:
    #"""Amount allocated to each player"""
    endowment = 100

    efficiency_factor = 1.8

    question_correct = 92


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'public_goods'





class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 3

    def set_payoffs(self):
        contributions = sum([p.contribution for p in self.get_players()])
        individual_share = contributions * Constants.efficiency_factor / self.players_per_group
        for p in self.get_players():
            p.points = (Constants.endowment - p.contribution) + individual_share
            p.payoff = p.points / 100


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    contribution = models.PositiveIntegerField(
        doc="""The amount contributed by the player""",
        widget=widgets.TextInput()
    )

    points = models.PositiveIntegerField(null=True)

    question = models.PositiveIntegerField(null=True, verbose_name='', widget=widgets.TextInput())
    feedbackq = models.CharField(null=True, verbose_name='How well do you think this sample game was implemented?', widget=widgets.RadioSelectHorizontal())

    def feedbackq_choices(self):
        return ['Very well', 'Well', 'OK', 'Badly', 'Very badly']

    def question_correct(self):
        return self.question == Constants.question_correct

    def contribution_error_message(self, value):
        if not 0 <= value <= Constants.endowment:
            return 'Your entry is invalid.'


