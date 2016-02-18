# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    pass

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass

class Results(Page):
    pass


page_sequence = [
    MyPage,
    ResultsWaitPage,
    Results
]
