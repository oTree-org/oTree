# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    timeout_seconds = 600
    def is_displayed(self):
        return  self.subsession.round_number == 2

class Guess(Page):

    def vars_for_template(self):
        return {
            'overthrow': 5
        }

page_sequence =[
    Introduction,
    Guess
]
