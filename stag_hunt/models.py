# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models


doc = """
Stag Hunt
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'stag_hunt'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    stag_stag_amount = models.MoneyField(
        default=0.20,
        doc="""
        Amount rewarded for choosing both stag
        """
    )
    stag_hare_amount = models.MoneyField(
        default=0.00,
        doc="""
        Amount rewarded for choosing stag and hare
        """
    )
    hare_stag_amount = models.MoneyField(
        default=0.10,
        doc="""
        Amount rewarded for choosing hare and stag
        """
    )
    hare_hare_amount = models.MoneyField(
        default=0.10,
        doc="""
        Amount rewarded for choosing both hare
        """
    )


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 2


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    decision = models.CharField(
        default=None,
        choices=['Stag', 'Hare'],
        doc='either Stag or Hare',
    )

    def other_player(self):
        """Returns other player in match"""
        return self.other_players_in_match()[0]

    def set_payoff(self):

        payoff_matrix = {
            'Stag': {
                'Stag': self.treatment.stag_stag_amount,
                'Hare': self.treatment.stag_hare_amount,
            },
            'Hare': {
                'Stag': self.treatment.hare_stag_amount,
                'Hare': self.treatment.hare_hare_amount,
            }
        }
        self.payoff = payoff_matrix[self.decision][self.other_player().decision]


def treatments():
    return [Treatment.create()]