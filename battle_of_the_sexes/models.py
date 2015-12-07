# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range
# </standard imports>


doc = """
This is a 2-player 2-strategy coordination game. The name and story originated
from
<a href="http://books.google.ch/books?id=uqDDAgAAQBAJ&lpg=PP1&ots=S-DC4LemnS&lr&pg=PP1#v=onepage&q&f=false" target="_blank">
    Luce and Raiffa (1957)
</a>.

"""

source_code = (
    "https://github.com/oTree-org/oTree/tree/master/battle_of_the_sexes"
)

bibliography = (
    (
        'Luce, R. Duncan, and Howard Raiffa. Games and decisions: '
        'Introduction and critical survey. Courier Dover Publications, 2012.'
    ),
    (
        'Rapoport, Anatol. Two-person game theory. Courier Dover '
        'Publications, 1999.'
    ),
    (
        'Cooper, Russell, et al. "Forward induction in the '
        'battle-of-the-sexes games."The American Economic Review (1993): '
        '1303-1316.'
    ),
    (
        'Cooper, Russell, et al. "Communication in the battle of the sexes '
        'game: some experimental results." The RAND Journal of Economics '
        '(1989): 568-587.'
    )
)


links = {
    "Wikipedia": {
        "Battle of the Sexes":
            "https://en.wikipedia.org/wiki/Battle_of_the_sexes_%28game_theory%29",
        "Coordination Game": "https://en.wikipedia.org/wiki/Coordination_game"
    }
}


keywords = ("Battle of the Sexes", "Coordination")


class Constants(BaseConstants):
    name_in_url = 'battle_of_the_sexes'
    players_per_group = 2
    num_rounds = 1

    # """Amount rewarded to husband if football is chosen"""
    football_husband_amount = opera_wife_amount = c(300)

    # Amount rewarded to wife if football is chosen
    football_wife_amount = opera_husband_amount = c(200)

    # amount rewarded to either if the choices don't match
    mismatch_amount = c(0)


    training_1_husband_correct = c(0)
    training_1_wife_correct = c(0)

    training_1_maximum_offered_points = c(300)
    fixed_pay = 10

class Subsession(BaseSubsession):

    pass


class Group(BaseGroup):



    def set_payoffs(self):
        husband = self.get_player_by_role('husband')
        wife = self.get_player_by_role('wife')

        if husband.decision != wife.decision:
            husband.payoff = Constants.mismatch_amount
            wife.payoff = Constants.mismatch_amount

        else:
            if husband.decision == 'Football':
                husband.payoff = Constants.football_husband_amount
                wife.payoff = Constants.football_wife_amount
            else:
                husband.payoff = Constants.opera_husband_amount
                wife.payoff = Constants.opera_wife_amount


class Player(BasePlayer):

    training_question_1_husband = models.CurrencyField(min=0, max=Constants.training_1_maximum_offered_points)

    training_question_1_wife = models.CurrencyField(min=0, max=Constants.training_1_maximum_offered_points)

    decision = models.CharField(
        choices=['Football', 'Opera'],
        doc="""Either football or the opera""",
        widget=widgets.RadioSelect()
    )

    def is_training_question_1_husband_correct(self):
        return (self.training_question_1_husband ==
                Constants.training_1_husband_correct)

    def is_training_question_1_wife_correct(self):
        return (self.training_question_1_wife ==
                Constants.training_1_wife_correct)

    def other_player(self):
        """Returns other player in group"""
        return self.get_others_in_group()[0]

    def role(self):
        if self.id_in_group == 1:
            return 'husband'
        if self.id_in_group == 2:
            return 'wife'


