# -*- coding: utf-8 -*-
import dictator.models as models
from dictator._builtin import Page, WaitPage


class Introduction(Page):

    template_name = 'dictator/Introduction.html'

    def variables_for_template(self):
        return {'allocated_amount': self.treatment.allocated_amount,
                'player_id': self.player.index_among_players_in_match}


class Offer(Page):

    template_name = 'dictator/Offer.html'

    form_model = models.Match
    form_fields = ['offer_amount']

    def participate_condition(self):
        return self.player.index_among_players_in_match == 1


class ResultsWaitPage(WaitPage):

    group = models.Match

    def after_all_players_arrive(self):
        self.match.set_payoffs()

    def body_text(self):
        if self.player.index_among_players_in_match == 2:
            return "Waiting for the dictator to make an offer."


class Results(Page):

    template_name = 'dictator/Results.html'

    def variables_for_template(self):
        return {'payoff': self.player.payoff,
                'offer_amount': self.match.offer_amount,
                'player_id': self.player.index_among_players_in_match}


def pages():

    return [Introduction,
            Offer,
            ResultsWaitPage,
            Results]
