from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
Each player decides if to free ride or to volunteer from which all will
benefit.

See: Diekmann, A. (1985). Volunteer's dilemma. Journal of Conflict
Resolution, 605-610.
"""


class Constants(BaseConstants):
    name_in_url = 'volunteer_dilemma'
    players_per_group = 3
    num_rounds = 1

    instructions_template = 'volunteer_dilemma/instructions.html'

    num_other_players = players_per_group - 1

    # """Payoff for each player if at least one volunteers"""
    general_benefit = c(100)

    # """Cost incurred by volunteering player"""
    volunteer_cost = c(40)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    num_volunteers = models.IntegerField()

    def set_payoffs(self):
        players = self.get_players()
        self.num_volunteers = sum([p.volunteer for p in players])
        if self.num_volunteers > 0:
            baseline_amount = Constants.general_benefit
        else:
            baseline_amount = c(0)
        for p in players:
            p.payoff = baseline_amount
            if p.volunteer:
                p.payoff -= Constants.volunteer_cost


class Player(BasePlayer):
    volunteer = models.BooleanField(
        doc="""Whether player volunteers""",
    )
