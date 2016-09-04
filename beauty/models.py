from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


doc = """
5 players guess what 2/3 of the average of their guesses will be; the one with
the closest guess wins.

See: Nagel, Rosemarie. "Unraveling in guessing games: An experimental
study. The American Economic Review (1995): 1313-1326.
"""


class Constants(BaseConstants):
    players_per_group = 5
    num_rounds = 1
    name_in_url = 'beauty'

    instructions_template = 'beauty/Instructions.html'

    winner_payoff = c(100)
    guess_max = 100


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    two_third_guesses = models.FloatField()
    best_guess = models.FloatField()
    tie = models.BooleanField(initial=False)

    def set_payoffs(self):
        players = self.get_players()
        self.two_third_guesses = (
            (2 / 3) * sum(p.guess_value for p in players) / len(players)
        )

        candidates = []
        smallest_difference_so_far = Constants.guess_max + 1  # initialize to largest possible difference
        tie = False
        for p in self.get_players():
            p.payoff = 0
            p.is_winner = False  # initialize to false
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
            p.is_winner = True
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
        min=0, max=Constants.guess_max,
        doc="""
        Each player guess: between 0-{}
        """.format(Constants.guess_max)
    )
