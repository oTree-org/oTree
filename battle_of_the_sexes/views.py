# -*- coding: utf-8 -*-
import battle_of_the_sexes.forms as forms
from battle_of_the_sexes.utilities import Page, MatchWaitPage, SubsessionWaitPage
from ptree.common import Money, money_range


class Decide(Page):

    def participate_condition(self):
        return True

    template_name = 'battle_of_the_sexes/Decide.html'

    def get_form_class(self):
        return forms.DecisionForm

    def variables_for_template(self):
        return {
            'role': self.participant.role(),
            'fbl_husband_amt': self.treatment.football_husband_amount,
            'fbl_wife_amt': self.treatment.football_wife_amount,
            'fbl_opr_amt': self.treatment.mismatch_amount,
            'opr_husband_amt': self.treatment.opera_husband_amount,
            'opr_wife_amt': self.treatment.opera_wife_amount
        }


class ResultsWaitPage(MatchWaitPage):

    def action(self):
        self.match.set_payoffs()

    def body_text(self):
        return "Waiting for the other participant."


class Results(Page):

    def participate_condition(self):
        return True

    template_name = 'battle_of_the_sexes/Results.html'

    def variables_for_template(self):

        return {
            'payoff': self.participant.payoff,
            'decision': self.participant.decision,
            'other_decision': self.participant.other_participant().decision,
        }


def pages():
    return [
        Decide,
        ResultsWaitPage,
        Results
    ]