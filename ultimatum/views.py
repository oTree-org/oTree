# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range

from ._builtin import Page, WaitPage
from . import models
from .models import Constants

#todo: replace global vars


class Introduction(Page):

    timeout_seconds = 600


class Offer(Page):

    form_model = models.Group
    form_fields = ['amount_offered']

    def is_displayed(self):
        return self.player.id_in_group == 1

    timeout_seconds = 600

class WaitForProposer(WaitPage):
    pass

class Accept(Page):

    form_model = models.Group
    form_fields = ['offer_accepted']

    def is_displayed(self):
        return self.player.id_in_group == 2 and not self.group.strategy


    timeout_seconds = 600


class AcceptStrategy(Page):

    form_model = models.Group
    form_fields = ['response_{}'.format(int(i)) for i in Constants.offer_choices]

    def is_displayed(self):
        return self.player.id_in_group == 2 and self.group.strategy


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    pass




page_sequence = [Introduction,
            Offer,
            WaitForProposer,
            Accept,
            AcceptStrategy,
            ResultsWaitPage,
            Results]

