# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range

from ._builtin import Page, WaitPage
from . import models
from .models import Constants

def variables_for_all_templates(self):
    return {
        'endowment': Constants.endowment,
        'reject_payoff': Constants.payoff_if_rejected,
        'strategy': self.group.strategy,
        'keep_give_amounts': Constants.keep_give_amounts,
        'offer_choices_count': len(Constants.offer_choices),

    }


class Introduction(Page):

    template_name = 'ultimatum/Introduction.html'


class Offer(Page):

    template_name = 'ultimatum/Offer.html'

    form_model = models.Group
    form_fields = ['amount_offered']

    def participate_condition(self):
        return self.player.id_in_group == 1

class WaitForProposer(WaitPage):
    pass

class Accept(Page):

    template_name = 'ultimatum/Accept.html'

    form_model = models.Group
    form_fields = ['offer_accepted']

    def participate_condition(self):
        return self.player.id_in_group == 2 and not self.group.strategy

    def variables_for_template(self):

        return {
            'amount_offered': self.group.amount_offered,
        }


class AcceptStrategy(Page):

    template_name = 'ultimatum/AcceptStrategy.html'

    form_model = models.Group
    form_fields = ['response_{}'.format(int(i)) for i in Constants.offer_choices]

    def participate_condition(self):
        return self.player.id_in_group == 2 and self.group.strategy


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    template_name = 'ultimatum/Results.html'


    def variables_for_template(self):

        return {
            'player_index': self.player.id_in_group,
            'amount_offered': self.group.amount_offered,
            'offer_accepted': self.group.offer_accepted,
            'payoff': self.player.payoff,
        }


def pages():

    return [Introduction,
            Offer,
            WaitForProposer,
            Accept,
            AcceptStrategy,
            ResultsWaitPage,
            Results]

