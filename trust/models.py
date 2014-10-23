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
This is a standard 2-player trust game where the amount sent by player 1 gets tripled. 
The trust game was first proposed by <a href="http://econweb.ucsd.edu/~jandreon/Econ264/papers/Berg%20et%20al%20GEB%201995.pdf" target="_blank">Berg, Dickhaut, and McCabe (1995)</a>.
<br />
Source code <a href="https://github.com/oTree-org/oTree/tree/master/trust"
target="_blank">here</a>.
"""

class Constants:

    #Initial amount allocated to each player
    amount_allocated = 100
    multiplication_factor = 3
    bonus = 10


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'trust'



class Group(otree.models.BaseGroup):


    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2

    sent_amount = models.PositiveIntegerField(
        doc="""Amount sent by P1""",
    )

    sent_back_amount = models.PositiveIntegerField(
        doc="""Amount sent back by P2""",
    )

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = p2.payoff = 0
        p1.points = Constants.bonus + Constants.amount_allocated\
            - self.sent_amount + self.sent_back_amount
        p2.points = Constants.bonus + self.sent_amount * Constants.multiplication_factor - self.sent_back_amount

    def sent_amount_error_message(self, value):
        if not 0 <= value <= Constants.amount_allocated:
            return 'Your entry is invalid.'

    def sent_back_amount_error_message(self, value):
        if not 0 <= value <= self.sent_amount * Constants.multiplication_factor:
            return 'Your entry is invalid.'


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>
    training_answer_x = models.PositiveIntegerField(
        null=True, verbose_name='Participant A would have')
    training_answer_y = models.PositiveIntegerField(
        null=True, verbose_name='Participant B would have')
    points = models.PositiveIntegerField()
    feedback = models.PositiveIntegerField(
        choices=(
            (5, 'Very well'),
            (4, 'Well'),
            (3, 'OK'),
            (2, 'Badly'),
            (1, 'Very badly')), widget=widgets.RadioSelectHorizontal(),
        verbose_name='')

    def role(self):
        return {1: 'A', 2: 'B'}[self.id_in_group]
