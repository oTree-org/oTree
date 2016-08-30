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
        yield SubmissionMustFail(views.Transcribe, {'transcribed_text': 'foo'})

        transcription = Constants.reference_texts[self.subsession.round_number - 1]
        if Constants.allowed_error_rates[self.subsession.round_number - 1] > 0:
            # add a 1-char error, should still be fine
            transcription += 'a'

        yield (views.Transcribe, {'transcribed_text': transcription})


        for value in [
            self.player.levenshtein_distance,
            self.player.transcribed_text,
            self.player.payoff
        ]:
            assert value != None

        if self.subsession.round_number == Constants.num_rounds:
            # final page should print lengths of all reference texts
            for ref_text in Constants.reference_texts:
                assert str(len(ref_text)) in self.html