# -*- coding: utf-8 -*-
import coordination.models as models
from coordination._builtin import Page, WaitPage


class Choice(Page):

    def participate_condition(self):
        return True

    template_name = 'coordination/Choice.html'

    def get_form_class(self):
        return forms.ChoiceForm

    def variables_for_template(self):
        return {'match_amount': self.treatment.match_amount,
                'mismatch_amount': self.treatment.mismatch_amount}


class ResultsWaitPage(WaitPage):

    group = models.Match

    def after_all_players_arrive(self):
        self.match.set_payoffs()

    def body_text(self):
        return "Waiting for the other player."


class Results(Page):

    def participate_condition(self):
        return True

    template_name = 'coordination/Results.html'

    def variables_for_template(self):
        return {'payoff': self.player.payoff,
                'choice': self.player.choice,
                'other_choice': self.player.other_player().choice,
                'same_choice': self.player.choice == self.player.other_player().choice}


def pages():

    return [Choice,
            ResultsWaitPage,
            Results]
