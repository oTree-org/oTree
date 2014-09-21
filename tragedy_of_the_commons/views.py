# -*- coding: utf-8 -*-
import otree.views
import otree.views.concrete
import tragedy_of_the_commons.forms as forms
from tragedy_of_the_commons._builtin import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range


class Decide(Page):

    def participate_condition(self):
        return True

    template_name = 'tragedy_of_the_commons/Decide.html'

    def get_form_class(self):
        return forms.DecideForm

    def variables_for_template(self):
        return {
            'common_share': self.treatment.common_share,
            'num_p': len(self.match.players),
        }


class ResultsWaitPage(MatchWaitPage):

    def after_all_players_arrive(self):
        self.match.set_payoffs()


class Results(Page):

    template_name = 'tragedy_of_the_commons/Results.html'

    def variables_for_template(self):
        return {
            'payoff': self.player.payoff,
        }


def pages():
    return [
        Decide,
        ResultsWaitPage,
        Results
    ]