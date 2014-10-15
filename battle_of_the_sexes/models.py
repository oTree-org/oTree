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

<h3>Recommended Literature</h3>
<ul>
    <li>Luce, R. Duncan, and Howard Raiffa. Games and decisions: Introduction and critical survey. Courier Dover Publications, 2012.</li>
    <li>Rapoport, Anatol. Two-person game theory. Courier Dover Publications, 1999.</li>
    <li>Cooper, Russell, et al. "Forward induction in the battle-of-the-sexes games."The American Economic Review (1993): 1303-1316.</li>
    <li>Cooper, Russell, et al. "Communication in the battle of the sexes game: some experimental results." The RAND Journal of Economics (1989): 568-587.</li>
</ul>

<strong>Wikipedia:</strong> Battle of the Sexes, Coordination Game<br/>
<strong>Keywords:</strong>
    <a target="_blank" href="https://duckduckgo.com/?q=Battle+of+the+Sexes+game+theory&t=otree"</a>
        <span class="badge">Battle of the Sexes</span>
    </a>,
    <a target="_blank" href="https://duckduckgo.com/?q=coordination+game+theory&t=otree"</a>
        <span class="badge badge-info">Coordination</span>
    </a>

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

    training_1_husband_correct = 0
    training_1_wife_correct = 0


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

    training_question_1_husband = models.PositiveIntegerField(
        null=True, verbose_name=''
    )
    training_question_1_wife = models.PositiveIntegerField(
        null=True, verbose_name=''
    )

    decision = models.CharField(
        doc="""Either football or the opera""",
        widget=widgets.RadioSelect()
    )

    def is_training_question_1_husband_correct(self):
        return (self.training_question_1_husband ==
                Constants.training_1_husband_correct)

    def is_training_question_1_wife_correct(self):
        return (self.training_question_1_wife ==
                Constants.training_1_wife_correct)

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


