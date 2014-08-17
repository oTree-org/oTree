# -*- coding: utf-8 -*-
import stag_hunt.forms as forms
from stag_hunt.utilities import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range


class Decide(Page):

    def participate_condition(self):
        return True

    template_name = 'stag_hunt/Decide.html'

    def get_form_class(self):
        return forms.DecisionForm

    def variables_for_template(self):
        return {
            'stag_stag': self.treatment.stag_stag_amount,
            'stag_hare': self.treatment.stag_hare_amount,
            'hare_stag': self.treatment.hare_stag_amount,
            'hare_hare': self.treatment.hare_hare_amount,
        }


class ResultsWaitPage(MatchWaitPage):

    def after_all_players_arrive(self):
        for p in self.match.players:
            p.set_payoff()

    def body_text(self):
        return "Waiting for the other player."


class Results(Page):

    def participate_condition(self):
        return True

    template_name = 'stag_hunt/Results.html'

    def variables_for_template(self):

        return {
            'payoff': self.player.payoff,
            'decision': self.player.decision,
            'other_decision': self.player.other_player().decision,
        }


def pages():
    return [
        Decide,
        ResultsWaitPage,
        Results
    ]