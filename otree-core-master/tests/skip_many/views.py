# -*- coding: utf-8 -*-
from __future__ import division, absolute_import

from otree.api import WaitPage

from tests.utils import BlankTemplatePage as Page

from .models import Constants


class MyPage(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [
    MyPage,
    ResultsWaitPage,
    Results
]
