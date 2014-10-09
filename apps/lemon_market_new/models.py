# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import division
"""Documentation at https://github.com/oTree-org/otree/wiki"""

from otree.db import models
import otree.models
from otree.common import Money, money_range


author = 'Your name here'

doc = """
Description of this app.
"""

class Subsession(otree.models.BaseSubsession):

    name_in_url = 'lemon_market_new'


class Group(otree.models.BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 1

    def set_payoffs(self):
        for p in self.players:
            p.payoff = 0 # change to whatever the payoff should be


class Player(otree.models.BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>

    def other_player(self):
        """Returns other player in group. Only valid for 2-player groupes."""
        return self.other_players_in_group()[0]

    # example field
    my_field = models.MoneyField(
        default=None,
        doc="""
        Description of this field, for documentation
        """
    )

    def my_field_error_message(self, value):
        if not 0 <= value <= 10:
            return 'Value is not in allowed range'


    def role(self):
        # you can make this depend of self.id_in_group
        return ''

