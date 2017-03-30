from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Demographics(Page):
    form_model = models.Player
    form_fields = ['age',
                   'gender']


class CognitiveReflectionTest(Page):
    form_model = models.Player
    form_fields = ['crt_bat',
                   'crt_widget',
                   'crt_lake']


page_sequence = [
    Demographics,
    CognitiveReflectionTest
]
