# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range

from ._builtin import Page, WaitPage
from . import models
from .models import Constants

#todo: replace global vars


class Introduction(Page):

    template_name = 'ultimatum/Introduction.html'

    timeout_seconds = 60


class Offer(Page):

    template_name = 'ultimatum/Offer.html'

    form_model = models.Group
    form_fields = ['amount_offered']

    def participate_condition(self):
        return self.player.id_in_group == 1

    timeout_seconds = 60

class WaitForProposer(WaitPage):
    pass

class Accept(Page):

    template_name = 'ultimatum/Accept.html'

    form_model = models.Group
    form_fields = ['offer_accepted']

    def participate_condition(self):
        return self.player.id_in_group == 2 and not self.group.strategy


    timeout_seconds = 60


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




page_sequence = [Introduction,
            Offer,
            WaitForProposer,
            Accept,
            AcceptStrategy,
            ResultsWaitPage,
            Results]

