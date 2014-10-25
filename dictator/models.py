# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from utils import FEEDBACK_CHOICES
# </standard imports>


doc = """
One player decides how to divide a certain amount between himself and the other
player.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/dictator"
target="_blank">here</a>.
"""
# Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness and the
# assumptions of economics." Journal of business (1986): S285-S300.
# Hoffman, Elizabeth, Kevin McCabe, and Vernon L. Smith. "Social distance and
# other-regarding behavior in dictator games." The American Economic
# Review(1996): 653-660.
# https://en.wikipedia.org/wiki/Dictator_game
# Keywords: Dictator Game, Fairness, Homo Economicus


class Constants:
    bonus = 10
    # Initial amount allocated to the dictator
    allocated_amount = 100


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'dictator'


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2

    kept = models.PositiveIntegerField(
        doc="""Amount dictator decided to keep for himself""",
        verbose_name='I will keep (from 0 to %i)' % Constants.allocated_amount
    )

    def kept_error_message(self, value):
        if not 0 <= value <= Constants.allocated_amount:
            return 'Your entry is invalid.'

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = Constants.bonus + self.kept
        p2.payoff = Constants.bonus + Constants.allocated_amount - self.kept


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    training_participant1_payoff = models.PositiveIntegerField(
        verbose_name="Participant 1's payoff would be")
    training_participant2_payoff = models.PositiveIntegerField(
        verbose_name="Participant 2's payoff would be")

    feedback = models.PositiveIntegerField(
        verbose_name='How well do you think this sample game was implemented?',
        choices=FEEDBACK_CHOICES, widget=widgets.RadioSelectHorizontal())
