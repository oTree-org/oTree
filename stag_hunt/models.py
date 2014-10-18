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
This is a 2-player 2-strategy coordination game. The original story was from <a href="https://en.wikipedia.org/wiki/Jean-Jacques_Rousseau" target="_blank">Jean-Jacques Rousseau</a>.
<br />
Source code <a href="https://github.com/oTree-org/oTree/tree/master/stag_hunt" target="_blank">here</a>.

<h3>Recommended Literature</h3>
<ul>
    <li>Skyrms, Brian. "The stag hunt." Proceedings and Addresses of the American Philosophical Association. American Philosophical Association, 2001.</li>
    <li>Battalio, Raymond, Larry Samuelson, and John Van Huyck. "Optimization incentives and coordination failure in laboratory stag hunt games."Econometrica 69.3 (2001): 749-764.</li>
</ul>

<p>
    <strong>Wikipedia:</strong>
    <a target="_blank" href="https://en.wikipedia.org/wiki/Stag_hunt">Stag Hunt</a>,&nbsp
    <a target="_blank" href="https://en.wikipedia.org/wiki/Coordination_game">Coordination Game</a>
</p>

<p>
    <strong>Keywords:</strong>
    <a target="_blank" href="https://duckduckgo.com/?q=Stag+Hunt+game+theory&t=otree"</a>
        <span class="badge">Stag Hunt</span>
    </a>,
    <a target="_blank" href="https://duckduckgo.com/?q=coordination+game+theory&t=otree"</a>
        <span class="badge badge-info">Coordination</span>
    </a>,
    <a target="_blank" href="https://duckduckgo.com/?q=cooperation+game+theory&t=otree"</a>
        <span class="badge badge-info">Cooperation</span>
    </a>,
        <a target="_blank" href="https://duckduckgo.com/?q=social+contract+game+theory&t=otree"</a>
        <span class="badge badge-info">Social Contract</span>
    </a>
</p>

"""

class Constants:
    stag_stag_amount = Money(0.20)
    stag_hare_amount = Money(0.00)
    hare_stag_amount = Money(0.10)
    hare_hare_amount = Money(0.10)

    training_question_1_my_payoff_correct = 0
    training_question_1_other_payoff_correct = 100
    training_1_maximun_offered_points = 200


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'stag_hunt'


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    training_question_1_my_payoff = models.PositiveIntegerField(
        null=True, verbose_name=''
    )
    training_question_1_other_payoff = models.PositiveIntegerField(
        null=True, verbose_name=''
    )

    decision = models.CharField(
        default=None,
        doc="""The player's choice""",
        widget=widgets.RadioSelect()
    )

    def is_training_question_1_my_payoff_correct(self):
        return (self.training_question_1_my_payoff==
                Constants.training_question_1_my_payoff_correct)

    def is_training_question_1_other_payoff_correct(self):
        return (self.training_question_1_other_payoff==
                Constants.training_question_1_other_payoff_correct)

    def training_question_1_my_payoff_error_message(self, value):
        if value > Constants.training_1_maximun_offered_points:
            msg = 'The payoff cannot be greater than points offered ({})'
            return msg.format(Constants.training_1_maximun_offered_points)

    def training_question_1_other_payoff_error_message(self, value):
        if value > Constants.training_1_maximun_offered_points:
            msg = 'The payoff cannot be greater than points offered ({})'
            return msg.format(Constants.training_1_maximun_offered_points)

    def decision_choices(self):
        return ['Stag', 'Hare']

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


