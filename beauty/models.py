# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>


doc = """
5 players guess what 2/3 of the average of their guesses will be; the one with
the closest guess wins.
"""


source_code = "https://github.com/oTree-org/oTree/tree/master/beauty"


bibliography = (
    (
        'Nagel, Rosemarie. "Unraveling in guessing games: An experimental '
        'study."The American Economic Review (1995): 1313-1326.'
    ),
    (
        'Bosch-Domenech, Antoni, et al. "One, two,(three), infinity,...: '
        'Newspaper and lab beauty-contest experiments." American Economic '
        'Review (2002): 1687-1701.'
    )
)


links = {
    "Wikipedia": {
        "Beauty Contest":
            "http://en.wikipedia.org/wiki/Keynesian_beauty_contest",
        "Guess 2/3 of the Average":
            "http://en.wikipedia.org/wiki/Guess_2/3_of_the_average"
    }
}


keywords = (
    "Beauty Contest", "Guessing Game", "Paradox",
    "Common Knowledge", "Rationality"
)


class Constants(BaseConstants):
    players_per_group = 5
    num_rounds = 1
    name_in_url = 'beauty'

    winner_payoff = c(100)
    guess_max = 100
    fixed_pay = c(10)

    training_question_1_win_pick_correct = 10
    training_question_1_my_payoff_correct = c(50)
    training_1_maximun_pick = 100
    training_1_maximun_offered_points = c(100)


class Subsession(BaseSubsession):

    pass


class Group(BaseGroup):



    two_third_guesses = models.FloatField()
    best_guess = models.FloatField()
    tie = models.BooleanField(initial=False)

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



class Player(BasePlayer):

    is_winner = models.BooleanField(
        initial=False,
        doc="""
        True if player had the winning guess
        """
    )

    guess_value = models.PositiveIntegerField(
        initial=None,
        min=0, max=Constants.guess_max,
        doc="""
        Each player guess: between 0-{}
        """.format(Constants.guess_max)
    )

    training_question_1_win_pick = models.PositiveIntegerField(min=0, max=Constants.training_1_maximun_pick)

    training_question_1_my_payoff = models.CurrencyField(min=0, max=Constants.training_1_maximun_offered_points)

    def is_training_question_1_win_pick_correct(self):
        return (self.training_question_1_win_pick ==
                Constants.training_question_1_win_pick_correct)

    def is_training_question_1_my_payoff_correct(self):
            return (self.training_question_1_my_payoff ==
                    Constants.training_question_1_my_payoff_correct)
