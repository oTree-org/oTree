# -*- coding: utf-8 -*-
import battle_of_the_sexes.forms as forms
from battle_of_the_sexes.utilities import Page, MatchWaitPage, SubsessionWaitPage
from ptree.common import currency


class Decide(Page):

    def participate_condition(self):
        return True

    template_name = 'battle_of_the_sexes/Decide.html'

    def get_form_class(self):
        return forms.DecisionForm

    def variables_for_template(self):
        return {
            'fbl_amt1': currency(self.treatment.football_amount1),
            'fbl_amt2': currency(self.treatment.football_amount2),
            'fbl_opr_amt': currency(self.treatment.football_opera_amount),
            'opr_amt1': currency(self.treatment.opera_amount1),
            'opr_amt2': currency(self.treatment.opera_amount2)
        }


class ResultsWaitPage(MatchWaitPage):

    def action(self):
        for p in self.match.participants():
            p.set_payoff()

    def body_text(self):
        return "Waiting for the other participant."


class Results(Page):

    def participate_condition(self):
        return True

    template_name = 'battle_of_the_sexes/Results.html'

    def variables_for_template(self):

        return {
            'payoff': currency(self.participant.payoff),
            'decision': self.participant.decision,
            'other_decision': self.participant.other_participant().decision,
        }


def pages():
    return [
        Decide,
        ResultsWaitPage,
        Results
    ]