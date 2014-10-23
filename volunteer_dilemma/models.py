# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from utils import FEEDBACK_CHOICES
# </standard imports>

doc = """
Each player decides if to free ride or to volunteer from which all will
benefit.

Source code <a
href="https://github.com/oTree-org/oTree/tree/master/volunteer_dilemma"
target="_blank">here</a>.
"""
# Recommended Literature
# Diekmann, Andreas.
# "Volunteer's dilemma." Journal of Conflict Resolution(1985):
# http://en.wikipedia.org/wiki/Volunteer%27s_dilemma


class Constants:
    bonus = 10

    # """Payoff for each player if at least one volunteers"""
    general_benefit = 100

    # """Cost incurred by volunteering player"""
    volunteer_cost = 40


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'volunteer_dilemma'


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 3

    def set_payoffs(self):
        baseline_amount = Constants.bonus
        if any(p.volunteer for p in self.get_players()):
            baseline_amount += Constants.general_benefit
        for p in self.get_players():
            p.payoff = baseline_amount
            if p.volunteer:
                p.payoff -= Constants.volunteer_cost


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    training_my_payoff = models.PositiveIntegerField(
        verbose_name='My payoff would be')

    volunteer = models.NullBooleanField(
        doc="""Whether player volunteers""",
        widget=widgets.RadioSelect(),
    )

    feedback = models.PositiveIntegerField(
        choices=FEEDBACK_CHOICES, widget=widgets.RadioSelectHorizontal(),
        verbose_name='')
