# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree import widgets
from otree.common import Currency as c, currency_range

# </standard imports>

doc = """
Each player decides if to free ride or to volunteer from which all will
benefit.
"""

bibliography = (
    (
        "Diekmann, A. (1985). Volunteer's dilemma. Journal of Conflict "
        "Resolution, 605-610."
    ),
)


class Constants(BaseConstants):
    name_in_url = 'volunteer_dilemma'
    players_per_group = 3
    num_rounds = 1

    instructions_template = 'volunteer_dilemma/Instructions.html'

    num_other_players = players_per_group - 1

    # """Payoff for each player if at least one volunteers"""
    general_benefit = c(100)

    # """Cost incurred by volunteering player"""
    volunteer_cost = c(40)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    def set_payoffs(self):
        if any(p.volunteer for p in self.get_players()):
            baseline_amount = Constants.general_benefit
        for p in self.get_players():
            p.payoff = baseline_amount
            if p.volunteer:
                p.payoff -= Constants.volunteer_cost


class Player(BasePlayer):
    volunteer = models.BooleanField(
        doc="""Whether player volunteers""",
    )
