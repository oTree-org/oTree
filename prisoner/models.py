from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
This is a one-shot "Prisoner's Dilemma". Two players are asked separately
whether they want to cooperate or defect. Their choices directly determine the
payoffs.
"""


class Constants(BaseConstants):
    name_in_url = 'prisoner'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'prisoner/Instructions.html'

    # payoff if 1 player defects and the other cooperates""",
    betray_payoff = c(300)
    betrayed_payoff = c(0)

    # payoff if both players cooperate or both defect
    both_cooperate_payoff = c(200)
    both_defect_payoff = c(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    cooperate = models.BooleanField(
        choices=[
            [False, 'Defect'],
            [True, 'Cooperate']
        ]
    )

    def decision_label(self):
        if self.cooperate:
            return 'cooperate'
        return 'defect'

    def other_player(self):
        return self.get_others_in_group()[0]

    def set_payoff(self):

        payoff_matrix = {
            True:
                {
                    True: Constants.both_cooperate_payoff,
                    False: Constants.betrayed_payoff
                },
            False:
                {
                    True: Constants.betray_payoff,
                    False: Constants.both_defect_payoff
                }
        }

        self.payoff = payoff_matrix[self.cooperate][self.other_player().cooperate]
