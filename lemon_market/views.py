# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from django.utils.safestring import mark_safe
from random import choice
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
        What would be the period payoffs for the sellers and the buyer for\
        this period?''')

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
                'buyer': [p.training_buyer_earnings, 45],
                'seller 1': [p.training_seller1_earnings, 65],
                'seller 2': [p.training_seller2_earnings, 50]},
            explanation=mark_safe(Question1.question + '''
            <strong>Solution:</strong> Earnings for the buyer would be\
            <strong>45 points</strong>, for seller 1 <strong>65\
            points</strong>, and for seller 2 <strong>50 points</strong>.'''))


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
        return dict(
            subsession=self.subsession, player=self.player,
            payoff=self.player.payoff, buyer=buyer,
            seller=buyer.choice and self.group.get_player_by_id(
                buyer.choice + 1))


class FeedbackQ(FeedbackQ, Page):
    form_model = models.Player


class FinalResults(Page):

    template_name = 'lemon_market/FinalResults.html'

    def participate_condition(self):
        return self.subsession.round_number == self.subsession.number_of_rounds

    def variables_for_template(self):
        while True:
            final = [p for p in self.player.me_in_all_rounds(
                ) if p.subsession.final]
            if final:
                break
            final = choice(
                self.subsession.previous_rounds() + [self.subsession])
            final.final = True
            # final.save()
        final, = final
        return dict(
            rnd=final, payoff=final.payoff + 10,
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
