from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


doc = """
A demo of how rounds work in oTree, in the context of 'matching pennies'
"""


class Constants(BaseConstants):
    name_in_url = 'matching_pennies'
    players_per_group = 2
    num_rounds = 4

    stakes = c(100)


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round
        if self.round_number == 3:
            # reverse the roles
            matrix = self.get_group_matrix()
            for row in matrix:
                row.reverse()
            self.set_group_matrix(matrix)
        if self.round_number > 3:
            self.group_like_round(3)


class Group(BaseGroup):
    def set_payoffs(self):
        matcher = self.get_player_by_role('Matcher')
        mismatcher = self.get_player_by_role('Mismatcher')

        if matcher.penny_side == mismatcher.penny_side:
            matcher.is_winner = True
            mismatcher.is_winner = False
        else:
            matcher.is_winner = False
            mismatcher.is_winner = True
        for player in [mismatcher, matcher]:
            if self.subsession.round_number == self.session.vars['paying_round'] and player.is_winner:
                player.payoff = Constants.stakes
            else:
                player.payoff = c(0)


class Player(BasePlayer):
    penny_side = models.StringField(
        choices=['Heads', 'Tails'],
        widget=widgets.RadioSelect
    )

    is_winner = models.BooleanField()

    def role(self):
        if self.id_in_group == 1:
            return 'Mismatcher'
        if self.id_in_group == 2:
            return 'Matcher'
