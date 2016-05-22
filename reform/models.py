# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json

# </standard imports>

author = 'Alex'

doc = """
reforming game
"""

class Constants(BaseConstants):
    name_in_url = 'reform'
    players_per_group = 2
    num_rounds = 3
    base_sales = 16
    base_consumption = 4
    reform_penalty = 4
    reform_benefits = 0.5
    approval_cost = 0.3
    solidarity_benefits = {0: 0.0, 1: 0.2, 2: 0.5, 3: 1, 4: 1.6, 5: 2.3}
    points_to_overthrow = 6
    max_overthrow_vote_for_player = 5
    max_reforms = 5
    losses_from_overthrow = 10
    losses_from_chaos = 5


class Subsession(BaseSubsession):

    # need to introduce reforms participant var in order for them to carry over to next rounds. The same thing with overthrow switch.
    # regarding reformed_this_round -- this is ugly, but I couldn't come up with a way to create indicator of whether a player was reformed this round without p.participant.vars
    def before_session_starts(self):
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars['reforms'] = 0
                p.participant.vars['reformed_this_round'] = 0
            self.session.vars['overthrow'] = 0
            self.session.vars['overthrow_round'] = 0
            self.session.vars['coordinated_reforms'] = 0
        self.session.vars['total_approvals'] = 0

class Group(BaseGroup):
    # before the overthrow, number of reforms is equal to round number
    def num_reforms(self):
        return self.subsession.round_number

    reformed_id = 0
    # pick one player to be reformed
    def reformed_player(self):
        while True:
            self.reformed_id = random.randint(1,Constants.players_per_group)
            if self.num_reforms() - self.get_player_by_id(self.reformed_id).participant.vars['reforms']*Constants.players_per_group > 0:
                break
        for p in self.get_players():
            if p.id_in_group == self.reformed_id:
                p.participant.vars['reforms'] += 1
                p.participant.vars['reformed_this_round'] = 1
            else:
                p.participant.vars['reformed_this_round'] = 0

    # counting approvals for the government to give according solidarity benefits to everybody
    def approvals(self):
        return sum(p.approval for p in self.get_players())

    def approvals_in_previous_round(self):
        return int(sum(p.in_previous_rounds()[-1].approval for p in self.get_players()))

    # sums up players votes for overthrow and switches regime, if necessary
    def total_votes_for_overthrow(self):
        if sum(p.vote_to_overthrow for p in self.get_players()) >= Constants.points_to_overthrow and self.session.vars['overthrow'] == 0:
            self.session.vars['overthrow'] = 1
            self.session.vars['overthrow_round'] = self.subsession.round_number
            # chaos loses or something
            for p in self.get_players():
                p.payoff -= Constants.losses_from_overthrow

        return sum(p.vote_to_overthrow for p in self.get_players())

    reforms_votes_group = []
    # aggregate proposed number of reforms (after overthrow mechanic)
    def reform(self):
        for p in self.get_players():
            self.reforms_votes_group.append(p.reforms_votes)

    def payoffs(self):
        # normal payoff
        if self.session.vars['overthrow'] == 0:
            for p in self.get_players():
                p.payoff = \
                    Constants.base_sales \
                    - ( p.participant.vars['reforms'] * Constants.reform_penalty ) \
                    + Constants.base_consumption \
                    + (( self.num_reforms() - p.participant.vars['reforms'] ) * Constants.reform_benefits) \
                    - ( p.approval * Constants.approval_cost ) \
                    + Constants.solidarity_benefits[self.approvals()] \
                    - p.vote_to_overthrow
        # payoff after overthrow if coordination of reforming achieved
        elif self.reforms_votes_group.count(self.reforms_votes_group[0]) == len(self.reforms_votes_group):
            self.session.vars['coordinated_reforms'] = self.reforms_votes_group[0]
            for p in self.get_players():
                p.payoff = \
                    Constants.base_sales \
                    + Constants.base_consumption \
                    + self.session.vars['coordinated_reforms'] * Constants.reform_benefits
        # payoff after overthrow if no coordination of reforming achieved
        else:
            self.session.vars['coordinated_reforms'] = 0
            for p in self.get_players():
                p.payoff = \
                    Constants.base_sales \
                    + Constants.base_consumption \
                    - Constants.losses_from_chaos


class Player(BasePlayer):

    # form showing whether a player approves government's reforms
    approval_choices = ((1, "Одобряю"),(0, "Не одобряю"))
    approval = models.FloatField(widget=widgets.RadioSelect, choices=approval_choices)

    # form showing how much a player is spending on trying to overthrow the system
    vote_to_overthrow = models.FloatField(widget=widgets.SliderInput(attrs={'step': '1'}), min=0, max=Constants.max_overthrow_vote_for_player, default=3)

    # form showing how much reforms a player desires after the overthrow
    reforms_votes = models.FloatField(widget=widgets.SliderInput(attrs={'step': '1'}), min=0, max=Constants.max_reforms, default=3)