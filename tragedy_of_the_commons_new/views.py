# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import division
import otree.views
import tragedy_of_the_commons_new.models as models
from tragedy_of_the_commons_new._builtin import Page, WaitPage
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

    template_name = 'tragedy_of_the_commons_new/MyPage.html'

    def variables_for_template(self):
        return {
            'my_variable_here': 1,
        }

class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        self.group.set_payoffs()

class Results(Page):

    template_name = 'tragedy_of_the_commons_new/Results.html'

def pages():
    return [
        Introduction,
        ResultsWaitPage,
        Results
    ]