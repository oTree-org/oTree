# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Currency as c, currency_range
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        self.submit(views.Transcription1, {'transcription_1': Constants.reference_texts[0]})
        self.submit(views.Transcription2, {'transcription_2': Constants.reference_texts[1]})

    def validate_play(self):
        pass