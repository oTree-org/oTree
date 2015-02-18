# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


def vars_for_all_templates(self):
    return {
        # example:
        #'my_field': self.player.my_field,
    }


class MyPage(Page):

    form_model = models.Player
    form_fields = ['my_field']

    def is_displayed(self):
        return True

    template_name = 'mturk_submit/MyPage.html'

    def vars_for_template(self):
        return {
            'my_variable_here': 1,
        }


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    template_name = 'mturk_submit/Results.html'


page_sequence =[
        MyPage,
        ResultsWaitPage,
        Results
    ]
