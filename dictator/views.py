# -*- coding: utf-8 -*-
from __future__ import division
import dictator.models as models
from dictator._builtin import Page, WaitPage


class Introduction(Page):

    template_name = 'dictator/Introduction.html'

    def variables_for_template(self):
        return {'allocated_amount': self.subsession.allocated_amount,
                'player_id': self.player.id_in_group}


class Offer(Page):

    template_name = 'dictator/Offer.html'

    form_model = models.Group
    form_fields = ['offer_amount']

    def participate_condition(self):
        return self.player.id_in_group == 1


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def body_text(self):
        if self.player.id_in_group == 2:
            return "Waiting for the dictator to make an offer."


class Results(Page):

    template_name = 'dictator/Results.html'

    def variables_for_template(self):
        return {'payoff': self.player.payoff,
                'offer_amount': self.group.offer_amount,
                'player_id': self.player.id_in_group}


def pages():

    return [Introduction,
            Offer,
            ResultsWaitPage,
            Results]
