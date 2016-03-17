# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random
import itertools

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>

author = 'Alex'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'reputation'
    players_per_group = 2
    num_rounds = 2

    endowment = c(100)
    multiplication_factor = 4

class Subsession(BaseSubsession):

    def before_session_starts(self):
        if self.round_number == 1:
            treatments = itertools.cycle(['sender', 'receiver'])
            for p in self.get_players():
                p.participant.vars['role'] = treatments.next()



class Group(BaseGroup):

    sent_amount = models.CurrencyField(min=50, max=Constants.endowment)
    sent_back_amount = models.CurrencyField()

    def set_payoffs(self):

        for p in self.get_players():
            if p.participant.vars['role'] == 'sender':
                p.payoff = Constants.endowment - self.sent_amount + self.sent_back_amount
            else:
                p.payoff = self.sent_amount * Constants.multiplication_factor - self.sent_back_amount


class Player(BasePlayer):
    pass