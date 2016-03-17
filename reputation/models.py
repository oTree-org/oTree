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

    # randombly assign players to be senders or receivers and by default list all as not uncooperative
    def before_session_starts(self):
        if self.round_number == 1:
            treatments = itertools.cycle(['sender', 'receiver'])
            for p in self.get_players():
                p.participant.vars['role'] = treatments.next()
                p.participant.vars['uncooperative'] = False



class Group(BaseGroup):

    sent = models.CurrencyField(min=50, max=Constants.endowment)
    sent_back = models.CurrencyField()
    bribe = models.CurrencyField()

    # money transferred by sender, multiplied
    def multiplication(self):
        return self.sent * Constants.multiplication_factor

    # fine receiver should pay. If positive, receiver returned less than half the money
    # maximum bribe = fine * 6
    def fine(self):
        return self.multiplication() * 0.5 - self.sent_back

    # determination of whether receiever pays the bribe, fine, or neither
    # if player pays the fine, they're marked as 'uncooperative' for future rounds.
    def fine_bribe(self):
        if random.random() > 0.0000001 and (self.fine() > 0):
            if self.bribe > random.randrange(0,self.fine()*6):
                return self.bribe
            else:
                self.get_player_by_id(2).participant.vars['uncooperative'] = True
                return self.fine()

        else:
            return c(0)

    # if player was found to be uncooperative, changes the message for player 1 in group on 'send' page
    def is_uncooperative(self):
        if self.get_player_by_id(2).participant.vars['uncooperative'] == True:
            return True
        else:
            return False



    # payoffs for each round
    def set_payoffs(self):

        for p in self.get_players():
            if p.participant.vars['role'] == 'sender':
                p.payoff = Constants.endowment - self.sent + self.sent_back
            else:
                p.payoff = self.sent * Constants.multiplication_factor - self.sent_back - self.fine_bribe()


class Player(BasePlayer):
    pass