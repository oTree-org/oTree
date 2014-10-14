# -*- coding: utf-8 -*-
from __future__ import division
import stag_hunt.models as models
from stag_hunt._builtin import Page, WaitPage


class Decide(Page):

    def participate_condition(self):
        return True

    template_name = 'stag_hunt/Decide.html'

    form_model = models.Player
    form_fields = ['decision']

    def variables_for_template(self):
        return {'player_index': self.player.id_in_group,
                'stag_stag': self.subsession.stag_stag_amount,
                'stag_hare': self.subsession.stag_hare_amount,
                'hare_stag': self.subsession.hare_stag_amount,
                'hare_hare': self.subsession.hare_hare_amount}


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()

    def body_text(self):
        return "Waiting for the other player."


class Results(Page):

    def participate_condition(self):
        return True

    template_name = 'stag_hunt/Results.html'

    def variables_for_template(self):

        return {'payoff': self.player.payoff,
                'decision': self.player.decision,
                'other_decision': self.player.other_player().decision,
                'decision_is_same': self.player.decision == self.player.other_player().decision}


def pages():

    return [Decide,
            ResultsWaitPage,
            Results]
