# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range

from ._builtin import Page, WaitPage
from . import models


#todo: replace global vars



class Offer(Page):

    form_model = models.Group
    form_fields = ['amount_offered']

    def is_displayed(self):
        return self.player.id_in_group == 1

    timeout_seconds = 180

class WaitForProposer(WaitPage):
    pass

class Accept(Page):

    form_model = models.Group
    form_fields = ['offer_accepted']

    def is_displayed(self):
        return self.player.id_in_group == 2


    timeout_seconds = 180





class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    pass




page_sequence = [
            Offer,
            WaitForProposer,
            Accept,
            ResultsWaitPage,
            Results]

