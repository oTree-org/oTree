# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range

from ._builtin import Page, WaitPage
from . import models
from .models import Constants

#todo: replace global vars

# def vars_for_all_templates(self):
#     return {
#         # 'endowment': Constants.endowment,
#         # 'reject_payoff': Constants.payoff_if_rejected,
#         # 'strategy': self.group.strategy,
#         # 'keep_give_amounts': Constants.keep_give_amounts,
#         #'offer_choices_count': Constants.offer_choices_count,
#
#     }


class Introduction(Page):

    template_name = 'ultimatum/Introduction.html'

    timeout_seconds = 10


class Offer(Page):

    template_name = 'ultimatum/Offer.html'

    form_model = models.Group
    form_fields = ['amount_offered']

    def is_displayed(self):
        return self.player.id_in_group == 1

    timeout_seconds = 10

class WaitForProposer(WaitPage):
    pass

class Accept(Page):

    template_name = 'ultimatum/Accept.html'

    form_model = models.Group
    form_fields = ['offer_accepted']

    def is_displayed(self):
        return self.player.id_in_group == 2 and not self.group.strategy


    timeout_seconds = 10


class AcceptStrategy(Page):

    template_name = 'ultimatum/AcceptStrategy.html'

    form_model = models.Group
    form_fields = ['response_{}'.format(int(i)) for i in Constants.offer_choices]

    def is_displayed(self):
        return self.player.id_in_group == 2 and self.group.strategy


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    template_name = 'ultimatum/Results.html'




page_sequence = [Introduction,
            Offer,
            WaitForProposer,
            Accept,
            AcceptStrategy,
            ResultsWaitPage,
            Results]

