# -*- coding: utf-8 -*-
from __future__ import division
import otree.views
import otree.views.concrete
import asset_market.forms as forms
from asset_market._builtin import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range

def variables_for_all_templates(self):
    return {
        # example:
        #'my_field': self.player.my_field,
    }

class Introduction(Page):

    def participate_condition(self):
        return True

    template_name = 'asset_market/MyPage.html'

    def get_form_class(self):
        return forms.MyForm

    def variables_for_template(self):
        return {
            'my_variable_here': 1,
        }

class ResultsWaitPage(MatchWaitPage):

    def after_all_players_arrive(self):
        self.match.set_payoffs()

class Results(Page):

    template_name = 'asset_market/Results.html'

def pages():
    return [
        Introduction,
        ResultsWaitPage,
        Results
    ]