# -*- coding: utf-8 -*-
from __future__ import division
import otree.views
import lemon_market_new.models as models
from lemon_market_new._builtin import Page, WaitPage
from otree.common import Money, money_range

def variables_for_all_templates(self):
    return {
        # example:
        #'my_field': self.player.my_field,
    }

class Introduction(Page):

    form_model = models.Player
    form_fields = ['my_field']

    def participate_condition(self):
        return True

    template_name = 'lemon_market_new/MyPage.html'

    def variables_for_template(self):
        return {
            'my_variable_here': 1,
        }

class ResultsWaitPage(WaitPage):

    group = models.Match

    def after_all_players_arrive(self):
        self.match.set_payoffs()

class Results(Page):

    template_name = 'lemon_market_new/Results.html'

def pages():
    return [
        Introduction,
        ResultsWaitPage,
        Results
    ]