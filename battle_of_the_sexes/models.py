# -*- coding: utf-8 -*-
from __future__ import division
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models
from otree import widgets


doc = """
In the battle of the sexes, two players are paired as a couple and must privately decide whether attend the opera or watch football.
The husband and wife prefer football and the opera, respectively, but both prefer to go to the same place rather than different ones.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/battle_of_the_sexes" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'battle_of_the_sexes'

    football_husband_amount = models.MoneyField(
        default=0.30,
        doc="""Amount rewarded to husband if football is chosen"""
    )
    football_wife_amount = models.MoneyField(
        default=0.20,
        doc="""Amount rewarded to wife if football is chosen"""
    )
    mismatch_amount = models.MoneyField(
        default=0.00,
        doc="""Amount rewarded for choosing football and opera for either players"""
    )
    opera_husband_amount = models.MoneyField(
        default=0.20,
        doc="""Amount rewarded to husband if opera is chosen"""
    )
    opera_wife_amount = models.MoneyField(
        default=0.30,
        doc="""Amount rewarded to wife if opera is chosen"""
    )




class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2

    def set_payoffs(self):
        husband = self.get_player_by_role('husband')
        wife = self.get_player_by_role('wife')

        if husband.decision != wife.decision:
            husband.payoff = self.subsession.mismatch_amount
            wife.payoff = self.subsession.mismatch_amount

        else:
            if husband.decision == 'Football':
                husband.payoff = self.subsession.football_husband_amount
                wife.payoff = self.subsession.football_wife_amount
            else:
                husband.payoff = self.subsession.opera_husband_amount
                wife.payoff = self.subsession.opera_wife_amount


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    decision = models.CharField(
        default=None,
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


