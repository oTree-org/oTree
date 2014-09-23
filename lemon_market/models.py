# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models
from otree.common import Money, money_range

author = 'Your name here'

doc = """
Description of this app.
"""

class Subsession(otree.models.BaseSubsession):

    name_in_url = 'lemon_market'


class Treatment(otree.models.BaseTreatment):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


class Match(otree.models.BaseMatch):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    treatment = models.ForeignKey(Treatment)
    # </built-in>

    players_per_match = 1

    def set_payoffs(self):
        for p in self.players:
            p.payoff = 0 # change to whatever the payoff should be


class Player(otree.models.BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    treatment = models.ForeignKey(Treatment, null = True)
    match = models.ForeignKey(Match, null = True)
    # </built-in>

    def other_player(self):
        """Returns other player in match. Only valid for 2-player matches."""
        return self.other_players_in_match()[0]

    # example field
    my_field = models.MoneyField(
        default=None,
        doc="""
        Description of this field, for documentation
        """
    )

    def role(self):
        # you can make this depend of self.index_among_players_in_match
        return ''

def treatments():
    return [Treatment.create()]