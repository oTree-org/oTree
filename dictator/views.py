# -*- coding: utf-8 -*-
import dictator.forms as forms
from dictator._builtin import Page, MatchWaitPage


class Introduction(Page):

    template_name = 'dictator/Introduction.html'

    def variables_for_template(self):
        return {'allocated_amount': self.treatment.allocated_amount,
                'player_id': self.player.index_among_players_in_match}


class Offer(Page):

    template_name = 'dictator/Offer.html'

    def get_form_class(self):
        return forms.OfferForm

    def participate_condition(self):
        return self.player.index_among_players_in_match == 1


class ResultsWaitPage(MatchWaitPage):

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
