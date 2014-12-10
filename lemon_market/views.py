# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from random import choice
from .models import Constants

def variables_for_all_templates(self):
    return {'instructions': 'lemon_market/Instructions.html'}


class Introduction(Page):

    template_name = 'global/Introduction.html'

    def participate_condition(self):
        return self.subsession.round_number == 1


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = [
        'training_buyer_earnings', 'training_seller1_earnings',
        'training_seller2_earnings']

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        return {'question_template': 'lemon_market/Question.html'}


class Feedback1(Page):
    template_name = 'lemon_market/Feedback.html'

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        p = self.player
        return {'answers': {
                'buyer': [p.training_buyer_earnings, 45],
                'seller 1': [p.training_seller1_earnings, 65],
                'seller 2': [p.training_seller2_earnings, 50]}}


class Production(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = ['quality', 'price']

    auto_submit_values = {'price': Constants.INITIAL, 'quality': 20}

    def participate_condition(self):
        return self.player.role().startswith('seller')

    def variables_for_template(self):
        return {
            'title': 'Production (Period %i of %i)' % (
                self.subsession.round_number,
                Constants.number_of_rounds),
            'question': 'You are %s.' % self.player.role()}


class Purchase(Page):
    template_name = 'lemon_market/Purchase.html'
    form_model = models.Player
    form_fields = ['choice']

    def participate_condition(self):
        return self.player.role() == 'buyer'

    def variables_for_template(self):
        return {'group': self.group, 'title': 'Purchase (Period %i of %i)' % (
            self.subsession.round_number, Constants.number_of_rounds)}

class SimpleWaitPage(WaitPage):
    pass

class ResultsWaitPage(WaitPage):


    def after_all_players_arrive(self):
        self.group.set_payoff()
        if self.subsession.round_number == Constants.number_of_rounds:
            final_subsession = choice(self.subsession.in_all_rounds())
            final_subsession.final = True
            final_subsession.save()


class Results(Page):

    template_name = 'lemon_market/Results.html'

    def variables_for_template(self):
        buyer = self.group.get_player_by_role('buyer')
        return {
            'subsession': self.subsession, 'player': self.player,
            'payoff': self.player.payoff, 'buyer': buyer,
            'number_of_rounds': Constants.number_of_rounds,
            'seller': buyer.choice and self.group.get_player_by_id(
                buyer.choice + 1)}


class FinalResults(Page):

    template_name = 'lemon_market/FinalResults.html'

    def participate_condition(self):
        return self.subsession.round_number == Constants.number_of_rounds

    def variables_for_template(self):
        for player in self.player.in_all_rounds():
            if player.subsession.final:
                break
        return {'player': player, 'payoff': player.payoff + 10,
                'group': self.group}


def pages():
    return [
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
