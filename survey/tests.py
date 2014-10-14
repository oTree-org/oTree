# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Money, money_range
from .models import Constants

class PlayerBot(Bot):

    def play(self):

        self.submit(views.Demographics, {
            'q_country': 'BS',
            'q_age': 24,
            'q_gender': 'Male'})

        self.submit(views.CognitiveReflectionTest, {
            'crt_bat_float': 0.10,
            'crt_widget': 5,
            'crt_lake': 48
        })

        self.submit(views.End)
