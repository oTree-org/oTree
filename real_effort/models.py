# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree import widgets
from otree import forms
from otree.common import Currency as c, currency_range
import random
from django.core.validators import MaxLengthValidator
# </standard imports>

doc = """
This is a task that requires real effort from participants. Subjects are shown two images of incomprehensible text. Subjects are required to transcribe (copy) the text into a text entry field. The quality of a subject's transcription is measured by the <a href="http://en.wikipedia.org/wiki/Levenshtein_distance">Levenshtein distance</a>.
"""

class Constants(BaseConstants):

    name_in_url = 'real_effort'
    players_per_group = None
    num_rounds = 1

    # error in case participant is not allowed to make any errors
    transcription_error_0 = "The transcription should be exactly the same as on the image."
    # error in case participant is allowed to make some errors, but not too many
    transcription_error_positive = "This transcription appears to contain too many errors."

    error_rate_transcription_1 = 0.0
    error_rate_transcription_2 = 0.3

    show_transcription_1 = False
    show_transcription_2 = True

    reference_texts = [
        "Revealed preference",
        "Hex ton satoha egavecen. Loh ta receso minenes da linoyiy xese coreliet ocotine! Senuh asud tu bubo tixorut sola, bo ipacape le rorisin lesiku etutale saseriec niyacin ponim na. Ri arariye senayi esoced behin? Tefid oveve duk mosar rototo buc: Leseri binin nolelar sise etolegus ibosa farare. Desac eno titeda res vab no mes!"
    ]
    transcription_max_length = max(len(text) for text in reference_texts) + 100
    paragraph_count = len(reference_texts)

    #text_reference_3 = "Niemawun ucosipof sec telel titoy su pogeh uwih! Munowu adonieq tebeli razet keqad iteg lih. Eceh renod ne ielirica fa nes da uhome! Na tacunel hili yeri rocesiev asutef tilapec li ibu! Yar fo te tuneruy osone rano hiyus ale covoses ememo! Ser balon domolof cenal tile neta rog epidierad."


def levenshtein(a, b):
    """Calculates the Levenshtein distance between a and b."""
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current = range(n + 1)
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous[j] + 1, current[j-1] + 1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]


def text_is_close_enough(text_user, text_reference, max_error_rate):
    error_threshold = len(text_reference) * max_error_rate
    distance = levenshtein(text_user, text_reference)
    return distance <= error_threshold


class Subsession(BaseSubsession):

    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):

    transcription_1 = models.TextField(validators=[MaxLengthValidator(Constants.transcription_max_length)])
    transcription_2 = models.TextField(validators=[MaxLengthValidator(Constants.transcription_max_length)])
    distance_1 = models.PositiveIntegerField()
    distance_2 = models.PositiveIntegerField()

    def set_payoff(self):
        self.payoff = 0
