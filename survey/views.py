# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

class Demographics(Page):

    template_name = 'survey/Survey_Demo.html'

    form_model = models.Player
    form_fields = ['q_country',
                  'q_age',
                  'q_gender']


class CognitiveReflectionTest(Page):

    template_name = 'survey/Survey_Cog.html'

    form_model = models.Player
    form_fields = ['crt_bat_float',
                  'crt_widget',
                  'crt_lake']

    def after_valid_form_submission(self):
        self.player.crt_bat = self.player.crt_bat_float * 100


class End(Page):

    def vars_for_template(self):
        self.player.set_payoff()
        return None


page_sequence = [Demographics,
            CognitiveReflectionTest,
            End]
