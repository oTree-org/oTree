# -*- coding: utf-8 -*-
import otree.views
import otree.views.concrete
import lemon_market.models as models
from lemon_market._builtin import Page, WaitPage
from otree.common import Money, money_range

def variables_for_all_templates(self):
    return {
        # example:
        #'my_field': self.player.my_field,
    }

class Introduction(Page):

    def participate_condition(self):
        return True

    template_name = 'lemon_market/MyPage.html'

    def get_form_class(self):
        return forms.MyForm

    def variables_for_template(self):
        return {
            'my_variable_here': 1,
        }

class ResultsWaitPage(WaitPage):

    group = models.Match

    def after_all_players_arrive(self):
        self.match.set_payoffs()

class Results(Page):

    template_name = 'lemon_market/Results.html'

def pages():
    return [
        Introduction,
        ResultsWaitPage,
        Results
    ]