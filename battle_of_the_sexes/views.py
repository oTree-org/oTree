# -*- coding: utf-8 -*-
import battle_of_the_sexes.forms as forms
from battle_of_the_sexes._builtin import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range


class Decide(Page):

    def participate_condition(self):
        return True

    template_name = 'battle_of_the_sexes/Decide.html'

    def get_form_class(self):
        return forms.DecisionForm

    def variables_for_template(self):
        return {
            'role': self.player.role(),
            'fbl_husband_amt': self.treatment.football_husband_amount,
            'fbl_wife_amt': self.treatment.football_wife_amount,
            'fbl_opr_amt': self.treatment.mismatch_amount,
            'opr_husband_amt': self.treatment.opera_husband_amount,
            'opr_wife_amt': self.treatment.opera_wife_amount
        }


class ResultsWaitPage(MatchWaitPage):

    def after_all_players_arrive(self):
        self.match.set_payoffs()

    def body_text(self):
        return "Waiting for the other player."


class Results(Page):

    def participate_condition(self):
        return True

    template_name = 'battle_of_the_sexes/Results.html'

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