# -*- coding: utf-8 -*-
from __future__ import division
import traveler_dilemma.models as models
from traveler_dilemma._builtin import Page, WaitPage


class Introduction(Page):

    template_name = 'traveler_dilemma/Introduction.html'

    def variables_for_template(self):
        return {'max_amount': self.subsession.max_amount,
                'min_amount': self.subsession.min_amount,
                'reward': self.subsession.reward,
                'penalty': self.subsession.penalty}


class Claim(Page):

    template_name = 'traveler_dilemma/Claim.html'

    form_model = models.Player
    form_fields = ['claim']


class ResultsWaitPage(WaitPage):

    group = models.Match

    def after_all_players_arrive(self):
        for p in self.match.players:
            p.set_payoff()


class Results(Page):

    template_name = 'traveler_dilemma/Results.html'

    def variables_for_template(self):
        return {
            'claim': self.player.claim,
            'other_claim': self.player.other_player().claim,
            'payoff': self.player.payoff
        }


def pages():

    return [Introduction,
            Claim,
            ResultsWaitPage,
            Results]