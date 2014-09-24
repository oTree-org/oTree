# -*- coding: utf-8 -*-
import survey.models as models
from survey._builtin import Page
from otree.common import Money


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


def pages():

    return [Demographics,
            CognitiveReflectionTest,
            End]
