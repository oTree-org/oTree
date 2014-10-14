# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Money, money_range
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

    template_name = 'survey/End.html'

    def variables_for_template(self):
        self.player.set_payoff()
        return None


def pages():

    return [Demographics,
            CognitiveReflectionTest,
            End]
