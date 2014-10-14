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
This is a 2-player 2-strategy coordination game. The name and story originated from <a href="http://books.google.ch/books?id=uqDDAgAAQBAJ&lpg=PP1&ots=S-DC4LemnS&lr&pg=PP1#v=onepage&q&f=false" target="_blank">Luce and Raiffa (1957)</a>.
<br />
Source code <a href="https://github.com/oTree-org/oTree/tree/master/battle_of_the_sexes" target="_blank">here</a>.
"""

class Constants:

    # """Amount rewarded to husband if football is chosen"""
    football_husband_amount = Money(0.30)

    # Amount rewarded to wife if football is chosen
    football_wife_amount = Money(0.20)

    # amount rewarded to either if the choices don't match
    mismatch_amount = Money(0.00)

    opera_husband_amount = Money(0.20)

    opera_wife_amount = Money(0.30)


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'battle_of_the_sexes'


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2

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


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    decision = models.CharField(
        doc="""Either football or the opera""",
        widget=widgets.RadioSelect()
    )

    def decision_choices(self):
        return ['Football', 'Opera']

    def other_player(self):
        """Returns other player in group"""
        return self.get_others_in_group()[0]

    def role(self):
        if self.id_in_group == 1:
            return 'husband'
        if self.id_in_group == 2:
            return 'wife'


