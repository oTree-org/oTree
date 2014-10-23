# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from django.utils.safestring import mark_safe
from utils import FeedbackQ


def variables_for_all_templates(self):
    return dict(instructions='lemon_market/Instructions.html')


class Introduction(Page):

    template_name = 'global/Introduction.html'

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        return {
            'payoff': self.player.payoff,
        }


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = 'training_buyer_earnings', 'training_seller1_earnings',\
        'training_seller2_earnings'
    question = mark_safe('''Suppose that the buyer saw the following listed\
        prices:
        <i>Price from Seller 1: 20 points</i>
        <i>Price from Seller 2: 20 points</i>
        The buyer then bought 1 unit from seller 1. Having completed the\
        purchase, the buyer realized that the commodity was of low grade.\
        What would be the earnings for the sellers and the buyer for this\
        period?''')

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        return dict(question=self.question)


class Feedback1(Page):
    template_name = 'global/Feedback.html'

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        p = self.player
        return dict(
            answers={
                'buyer': [p.training_buyer_earnings, -5],
                'seller 1': [p.training_seller1_earnings, 15],
                'seller 2': [p.training_seller2_earnings, 0]},
            explanation=mark_safe(Question1.question + '''
            <strong>Solution:</strong> Earnings for the buyer would be\
            -5 points, for seller 1 15 points, and for seller 2 0 points.'''))


class Production(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = 'quality', 'price'

    def participate_condition(self):
        return self.player.role().startswith('seller')

    def variables_for_template(self):
        return dict(
            title='Production (Period %i of %i)' % (
                self.subsession.round_number,
                self.subsession.number_of_rounds),
            question='You are %s.' % self.player.role())


class Purchase(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = 'choice',

    def participate_condition(self):
        return self.player.role() == 'buyer'

    def variables_for_template(self):
        return dict(title='Purchase (Period %i of %i)' % (
                    self.subsession.round_number,
                    self.subsession.number_of_rounds), question=mark_safe(
            '''You are %s.
            <strong>Below are the listed prices from the sellers:</strong>
            %s''' % (self.player.role(), '\n'.join(
                '<i>Price from %s: %i points</i>' % (
                    seller.role().capitalize(), seller.price)
                for seller in self.group.get_players()
                if seller.role().startswith('seller')))))


class WaitPage(WaitPage):
    scope = models.Group


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoff()


class Results(Page):

    template_name = 'lemon_market/Results.html'

    def variables_for_template(self):
        buyer = self.group.get_player_by_role('buyer')
        ctx = dict(
            subsession=self.subsession, player=self.player,
            payoff=self.player.payoff, buyer=buyer,
            seller=buyer.choice and self.group.get_player_by_id(
                buyer.choice + 1))
        if buyer.choice:
            ctx['seller'] = seller = self.group.get_player_by_id(
                buyer.choice + 1)
            if buyer == self.player:
                ctx['earnings'] = seller.quality - seller.price + 5
            else:
                ctx['earnings'] = seller.price - seller.quality
        return ctx


class FeedbackQ(FeedbackQ, Page):
    form_model = models.Player


class FinalResults(Page):

    template_name = 'lemon_market/FinalResults.html'

    def participate_condition(self):
        return self.subsession.round_number == self.subsession.number_of_rounds

    def variables_for_template(self):
        holding = sum([
            p.payoff for p in self.player.me_in_all_rounds()])
        return dict(
            holding=holding,
            total_payoff=holding + 10,
            player=self.player, group=self.group,
            rounds=self.subsession.previous_rounds() + [self.subsession])


def pages():
    return [
        Introduction,
        Question1,
        Feedback1,
        Production,
        WaitPage,
        Purchase,
        ResultsWaitPage,
        Results,
        FinalResults,
        FeedbackQ,
    ]
