# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Submit(Page):
    
    def before_next_page(self):
        self.player.payoff = 5

page_sequence =[
        Submit
    ]
