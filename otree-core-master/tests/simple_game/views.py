# -*- coding: utf-8 -*-
from __future__ import division, absolute_import
from . import models
from otree.api import WaitPage
from tests.utils import BlankTemplatePage as Page
from .models import Constants

class MyPage(Page):

    form_fields = ['my_field']
    form_model = models.Player

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

class Results(Page):
    pass

page_sequence = [
        MyPage,
        ResultsWaitPage,
        Results
    ]
