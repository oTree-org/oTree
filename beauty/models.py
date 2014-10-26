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
5 players guess what 2/3 of the average of their guesses will be; the one with the closest guess wins.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/beauty" target="_blank">here</a>.

<h3>Recommended Literature</h3>
<ul>
    <li>Nagel, Rosemarie. "Unraveling in guessing games: An experimental study."The American Economic Review (1995): 1313-1326.</li>
    <li>Bosch-Domenech, Antoni, et al. "One, two,(three), infinity,...: Newspaper and lab beauty-contest experiments." American Economic Review (2002): 1687-1701.</li>
</ul>

<p>
    <strong>Wikipedia:</strong>
    <a target="_blank" href="http://en.wikipedia.org/wiki/Keynesian_beauty_contest">Beauty Contest</a>,&nbsp
    <a target="_blank" href="http://en.wikipedia.org/wiki/Guess_2/3_of_the_average">Guess 2/3 of the Average</a>
</p>

<p>
    <strong>Keywords:</strong>
    <a target="_blank" href="https://duckduckgo.com/?q=Beauty+Contest+game+theory&t=otree"</a>
        <span class="badge">Beauty Contest</span>
    </a>,
    <a target="_blank" href="https://duckduckgo.com/?q=Guessing+game+theory&t=otree"</a>
        <span class="badge badge-info">Guessing Game</span>
    </a>
    <a target="_blank" href="https://duckduckgo.com/?q=paradox+game+theory&t=otree"</a>
        <span class="badge badge-info">Paradox</span>
    </a>
    <a target="_blank" href="https://duckduckgo.com/?q=Common+knowledge+game+theory&t=otree"</a>
        <span class="badge badge-info">Common Knowledge</span>
    </a>
    <a target="_blank" href="https://duckduckgo.com/?q=Rationality+game+theory&t=otree"</a>
        <span class="badge badge-info">Rationality</span>
    </a>
</p>

"""

class Constants:
    winner_payoff = 100
    guess_max = 100

    training_question_1_win_pick_correct = 10
    training_question_1_my_payoff_correct = 50
    training_1_maximun_pick = 100
    training_1_maximun_offered_points = 100


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'beauty'


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 5

    two_third_guesses = models.FloatField()
    best_guess = models.FloatField()
    tie = models.BooleanField(default=False)

    def set_payoffs(self):
        players = self.get_players()
        self.two_third_guesses = (
            (2/3) * sum(p.guess_value for p in players) / len(players)
        )

        candidates = []
        smallest_difference_so_far = Constants.guess_max + 1   # initialize to largest possible difference
        tie = False
        for p in self.get_players():
            p.payoff = 0
            p.is_winner = False # initialize to false
            difference = abs(p.guess_value - self.two_third_guesses)
            if difference < smallest_difference_so_far:
                tie = False
                candidates = [p]
                smallest_difference_so_far = difference
            elif difference == smallest_difference_so_far:
                tie = True
                candidates.append(p)

        self.tie = tie
        winners = candidates
        winners_cnt = len(winners)
        for p in winners:
            p.is_winner=True
            p.payoff = (
                Constants.winner_payoff / winners_cnt
                if tie else
                Constants.winner_payoff
            )

        self.best_guess = winners[0].guess_value



class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    is_winner = models.BooleanField(
        default=False,
        doc="""
        True if player had the winning guess
        """
    )

    guess_value = models.PositiveIntegerField(
        default=None,
        doc="""
        Each player guess: between 0-{}
        """.format(Constants.guess_max)
    )

    training_question_1_win_pick = models.PositiveIntegerField(
        null=True, verbose_name=''
    )
    training_question_1_my_payoff = models.PositiveIntegerField(
        null=True, verbose_name=''
    )

    def guess_value_error_message(self, value):
        if value > Constants.guess_max:
            msg = 'The value must be between 0 and {}'
            return msg.format(Constants.guess_max)

    def training_question_1_win_pick_error_message(self, value):
        if value > Constants.training_1_maximun_pick:
            msg = 'You can\' choice a number higher than 100'
            return msg.format(Constants.training_1_maximun_offered_points)

    def training_question_1_my_payoff_error_message(self, value):
        if value > Constants.training_1_maximun_offered_points:
            msg = 'The payoff cannot be greater than points offered ({})'
            return msg.format(Constants.training_1_maximun_offered_points)

    def is_training_question_1_win_pick_correct(self):
        return (self.training_question_1_win_pick ==
                Constants.training_question_1_win_pick_correct)

    def is_training_question_1_my_payoff_correct(self):
            return (self.training_question_1_my_payoff ==
                    Constants.training_question_1_my_payoff_correct)
