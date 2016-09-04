from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants

class Demographics(Page):

    form_model = models.Player
    form_fields = ['q_country',
                  'q_age',
                  'q_gender']


class CognitiveReflectionTest(Page):

    form_model = models.Player
    form_fields = ['crt_bat',
                  'crt_widget',
                  'crt_lake']

    def before_next_page(self):
        self.player.set_payoff()

page_sequence = [
    Demographics,
    CognitiveReflectionTest
]
