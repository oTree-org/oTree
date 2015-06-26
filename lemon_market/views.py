# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from random import choice
from .models import Constants
from otree.common import safe_json

def vars_for_all_templates(self):
    return {'instructions': 'lemon_market/Instructions.html'}


class Introduction(Page):

    template_name = 'global/Introduction.html'

    def is_displayed(self):
        return self.subsession.round_number == 1


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = [
        'training_buyer_earnings', 'training_seller1_earnings',
        'training_seller2_earnings']

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {'question_template': 'lemon_market/Question.html'}


class Feedback1(Page):
    template_name = 'lemon_market/Feedback.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        p = self.player
        return {'answers': {
                'buyer': [p.training_buyer_earnings, 45],
                'seller 1': [p.training_seller1_earnings, 60],
                'seller 2': [p.training_seller2_earnings, 50]}}


class Production(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = ['quality', 'price']

    timeout_submission = {'price': Constants.INITIAL, 'quality': 20}

    def is_displayed(self):
        return self.player.role().startswith('seller')

    def vars_for_template(self):
        return {
            'title': 'Production (Period %i of %i)' % (
                self.subsession.round_number,
                Constants.num_rounds),
            'question': 'You are %s.' % self.player.role()}

class SimpleWaitPage(WaitPage):
    pass

class Purchase(Page):

    form_model = models.Player
    form_fields = ['choice']

    def is_displayed(self):
        return self.player.role() == 'buyer'


    def vars_for_template(self):
        return {
            'title': 'Purchase (Period %i of %i)' % (self.subsession.round_number, Constants.num_rounds)
            }

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
        data = {'old_player': player,
                'payoff': player.payoff + Constants.participation_fee,
                'participation_fee': Constants.participation_fee}
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
            data['series'].append({'name': 'Earnings for %s' % player.role().capitalize(),
                                   'data': payoffs})
        data['series'] = safe_json(data['series'])
        return data


page_sequence = [
        Introduction,
        Question1,
        Feedback1,
        Production,
        SimpleWaitPage,
        Purchase,
        ResultsWaitPage,
        Results,
        FinalResults,
    ]
