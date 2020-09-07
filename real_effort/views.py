# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range, safe_json
from .models import Constants, levenshtein, text_is_close_enough
from django.conf import settings


def vars_for_all_templates(self):

    return {'paragraph_count': Constants.paragraph_count}


class Transcription1(Page):

    template_name = 'real_effort/Transcription.html'

    form_model = models.Player
    form_fields = ['transcription_1']

    def vars_for_template(self):
        return {
                'number': 1,
                'magic_link': settings.DEBUG and Constants.show_transcription_1,
                'transcription': Constants.reference_texts[0],
                'debug': settings.DEBUG,
                'error_rate_percent': int(100 * Constants.error_rate_transcription_1)

        }

    def transcription_1_error_message(self, text_user):
        if not text_is_close_enough(text_user, Constants.reference_texts[0], Constants.error_rate_transcription_1):
            if Constants.error_rate_transcription_1 == 0.0:
                return Constants.transcription_error_0
            else:
                return Constants.transcription_error_positive
        else:
            self.distance_1 = levenshtein(Constants.reference_texts[0], text_user)


class Transcription2(Page):

    template_name = 'real_effort/Transcription.html'

    form_model = models.Player
    form_fields = ['transcription_2']

    def vars_for_template(self):
        return {'number': 2,
                'magic_link': settings.DEBUG and Constants.show_transcription_2,
                'transcription': Constants.reference_texts[1],
                'error_rate_percent': int(100 * Constants.error_rate_transcription_2)}

    def transcription_2_error_message(self, text_user):
        if not text_is_close_enough(text_user, Constants.reference_texts[1], Constants.error_rate_transcription_2):
            if Constants.error_rate_transcription_2 == 0.0:
                return Constants.transcription_error_0
            else:
                return Constants.transcription_error_positive
        else:
            self.distance_2 = levenshtein(Constants.reference_texts[1], text_user)


class Summary(Page):

    def vars_for_template(self):
        self.player.set_payoff()
        return {
                #'distance_1' : self.player.distance_1,
                'transcription_entered_1' : len(self.player.transcription_1),
                'transcription_length_1' : len(Constants.reference_texts[0]),
                #'distance_2' : self.player.distance_2,
                'transcription_entered_2' : len(self.player.transcription_2),
                'transcription_length_2' : len(Constants.reference_texts[1]),
        }

page_sequence = [Transcription1,
            Transcription2,
            Summary]
