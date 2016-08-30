# -*- coding: utf-8 -*-
from __future__ import division
from . import views
from ._builtin import Bot
import random
from otree.common import Currency as c, currency_range
from .models import Constants
from otree.api import SubmissionMustFail

class PlayerBot(Bot):

    def play_round(self):
        # must reject transcription that is too inaccurate
        yield SubmissionMustFail(views.Transcription1, {'transcription_1': 'foo'})
        yield (views.Transcription1, {'transcription_1': Constants.reference_texts[0]})
        yield (views.Transcription2, {'transcription_2': Constants.reference_texts[1]})
