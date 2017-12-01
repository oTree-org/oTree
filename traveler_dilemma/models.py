from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
Kaushik Basu's famous traveler's dilemma (
<a href="http://www.jstor.org/stable/2117865" target="_blank">
    AER 1994
</a>).
It is a 2-player game. The game is framed as a traveler's dilemma and intended
for classroom/teaching use.
"""


class Constants(BaseConstants):
    name_in_url = 'traveler_dilemma'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'traveler_dilemma/Instructions.html'

    # Player's reward for the lowest claim"""
    adjustment_abs = c(2)

    # Player's deduction for the higher claim

    # The maximum claim to be requested
    max_amount = c(100)

    # The minimum claim to be requested
    min_amount = c(2)



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    lower_claim = models.CurrencyField()

    def set_payoffs(self):
        p1, p2 = self.get_players()
        if p1.claim == p2.claim:
            self.lower_claim = p1.claim
            for p in [p1, p2]:
                p.payoff = self.lower_claim
                p.adjustment = c(0)
        else:
            if p1.claim < p2.claim:
                winner, loser = p1, p2
            else:
                winner, loser = p2, p1
            self.lower_claim = winner.claim
            winner.adjustment = Constants.adjustment_abs
            loser.adjustment = -Constants.adjustment_abs
            winner.payoff = self.lower_claim + winner.adjustment
            loser.payoff = self.lower_claim + loser.adjustment


class Player(BasePlayer):
    # claim by player
    claim = models.CurrencyField(
        min=Constants.min_amount, max=Constants.max_amount,
        doc="""
        Each player's claim
        """
    )

    adjustment = models.CurrencyField()

    def other_player(self):
        return self.get_others_in_group()[0]


