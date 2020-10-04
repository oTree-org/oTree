from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


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
        import random

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
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        is_match = p1.penny_side == p2.penny_side

        for p in [p1, p2]:
            # a simpler way to write these 4 lines would be:
            # p.is_winner = (p.is_matcher() == is_match)
            if p.is_matcher() == is_match:
                p.is_winner = True
            else:
                p.is_winner = False
            if (
                self.subsession.round_number == self.session.vars['paying_round']
                and p.is_winner
            ):
                p.payoff = Constants.stakes
            else:
                p.payoff = c(0)


class Player(BasePlayer):
    penny_side = models.StringField(
        choices=[['Heads', 'Heads'], ['Tails', 'Tails']],
        widget=widgets.RadioSelect,
        label="I choose:",
    )

    is_winner = models.BooleanField()

    def is_matcher(self):
        return self.id_in_group == 1
