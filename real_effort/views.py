# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range, safe_json
from .models import Constants
from django.conf import settings


def vars_for_all_templates(self):

    return {'paragraph_count': Constants.paragraph_count}


class Transcription1(Page):

    template_name = 'real_effort/Transcription.html'

    form_model = models.Player
    form_fields = ['transcription_1']

    def vars_for_template(self):
        return {'number': 1,
                'magic_link': settings.DEBUG and Constants.show_transcription_1,
                'transcription': Constants.reference_texts[0],
                'debug': settings.DEBUG,
                'error_rate_percent': int(100 * Constants.error_rate_transcription_1)}


class Transcription2(Page):

    template_name = 'real_effort/Transcription.html'

    form_model = models.Player
    form_fields = ['transcription_2']

    def vars_for_template(self):
        return {'number': 2,
                'magic_link': settings.DEBUG and Constants.show_transcription_2,
                'transcription': Constants.reference_texts[1],
                'debug': settings.DEBUG,
                'error_rate_percent': int(100 * Constants.error_rate_transcription_2)}


class Summary(Page):

    template_name = 'real_effort/Summary.html'

    def vars_for_template(self):
        self.player.set_payoff()
        return {
                'distance_1' : self.player.distance_1,
                'transcription_entered_1' : len(self.player.transcription_1),
                'transcription_length_1' : len(Constants.reference_texts[0]),
                'distance_2' : self.player.distance_2,
                'transcription_entered_2' : len(self.player.transcription_2),
                'transcription_length_2' : len(Constants.reference_texts[1]),
        }

def pages():

    return [Transcription1,
            Transcription2,
            Summary]
