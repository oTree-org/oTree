# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree import widgets
import random
from otree.common import Currency as c, currency_range
# </standard imports>


doc = """
This is a 2-player 2-strategy coordination game. The original story was from
<a href="https://en.wikipedia.org/wiki/Jean-Jacques_Rousseau" target="_blank">
    Jean-Jacques Rousseau
</a>.
"""


source_code = "https://github.com/oTree-org/oTree/tree/master/stag_hunt"


bibliography = (
    (
        'Skyrms, Brian. "The stag hunt." Proceedings and Addresses of the '
        'American Philosophical Association. American Philosophical '
        'Association, 2001.'
    ),
    (
        'Battalio, Raymond, Larry Samuelson, and John Van Huyck. '
        '"Optimization incentives and coordination failure in laboratory stag '
        'hunt games."Econometrica 69.3 (2001): 749-764.'
    )
)


links = {
    "Wikipedia": {
        "Stag Hunt": "https://en.wikipedia.org/wiki/Stag_hunt",
        "Coordination Game": "https://en.wikipedia.org/wiki/Coordination_game"
    }
}


keywords = ("Stag Hunt", "Coordination", "Cooperation", "Social Contract")


class Constants(BaseConstants):
    name_in_url = 'stag_hunt'
    players_per_group = 2
    num_rounds = 1

    fixed_pay = c(10)

    stag_stag_amount = c(200)
    stag_hare_amount = c(0)
    hare_stag_amount = c(100)
    hare_hare_amount = c(100)


    training_question_1_my_payoff_correct = c(0)
    training_question_1_other_payoff_correct = c(100)
    training_1_maximun_offered_points = c(200)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):

    training_question_1_my_payoff = models.CurrencyField(min=0, max=Constants.training_1_maximun_offered_points)

    training_question_1_other_payoff = models.CurrencyField(min=0, max=Constants.training_1_maximun_offered_points)

    decision = models.CharField(
        choices=['Stag', 'Hare'],
        doc="""The player's choice""",
        widget=widgets.RadioSelect()
    )

    def is_training_question_1_my_payoff_correct(self):
        return (self.training_question_1_my_payoff==
                Constants.training_question_1_my_payoff_correct)

    def is_training_question_1_other_payoff_correct(self):
        return (self.training_question_1_other_payoff==
                Constants.training_question_1_other_payoff_correct)

    def other_player(self):
        """Returns other player in group"""
        return self.get_others_in_group()[0]

    def set_payoff(self):

        payoff_matrix = {
            'Stag': {
                'Stag': Constants.stag_stag_amount,
                'Hare': Constants.stag_hare_amount,
            },
            'Hare': {
                'Stag': Constants.hare_stag_amount,
                'Hare': Constants.hare_hare_amount,
            }
        }
        self.payoff = payoff_matrix[self.decision][self.other_player().decision]


