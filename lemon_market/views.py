# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from random import choice
from .models import Constants
from otree.common import safe_json


class Introduction(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class Production(Page):
    form_model = models.Player
    form_fields = ['quality', 'price']

    timeout_submission = {'price': Constants.INITIAL, 'quality': 20}

    def is_displayed(self):
        return self.player.role().startswith('seller')


class SimpleWaitPage(WaitPage):
    pass


class Purchase(Page):
    form_model = models.Player
    form_fields = ['choice']

    def is_displayed(self):
        return self.player.role() == 'buyer'


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoff()
        if self.subsession.round_number == Constants.num_rounds:
            final_subsession = choice(self.subsession.in_all_rounds())
            final_subsession.final = True
            final_subsession.save()


class Results(Page):
    def vars_for_template(self):
        buyer = self.group.get_player_by_role('buyer')

        return {
            'buyer': buyer,
            'seller': buyer.choice and self.group.get_player_by_id(
                buyer.choice + 1)
        }


class FinalResults(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        for player in self.player.in_all_rounds():
            if player.subsession.final:
                break
        data = {'old_player': player}
        #
        # Filling the data for graph
        #
        # transaction price for each round (None if no transaction happened)
        transaction_price = []
        for round in self.player.in_all_rounds():
            if round.group.seller():
                transaction_price.append(round.group.seller().price)
            else:
                transaction_price.append(None)
        data['series'] = list()
        data['series'].append({'name': 'Transaction Price',
                               'data': transaction_price})
        # payoffs for both buyer and sellers in each round
        for player in self.group.get_players():
            payoffs = []
            for round in player.in_all_rounds():
                payoffs.append(round.payoff)
            data['series'].append(
                {'name': 'Earnings for %s' % player.role().capitalize(),
                 'data': payoffs})
        data['series'] = safe_json(data['series'])
        return data


page_sequence = [
    Introduction,
    Production,
    SimpleWaitPage,
    Purchase,
    ResultsWaitPage,
    Results,
    FinalResults,
]
