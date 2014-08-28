# -*- coding: utf-8 -*-
import survey.forms as forms
from survey._builtin import Page


class Demographics(Page):

    form_class = forms.DemographicsForm
    template_name = 'survey/Survey.html'


class CognitiveReflectionTest(Page):

    form_class = forms.CognitiveReflectionTestForm
    template_name = 'survey/Survey.html'

    def after_valid_form_submission(self):
        self.player.crt_bat = self.player.crt_bat_float * 100


class End(Page):

    template_name = 'survey/End.html'


def pages():

    return [Demographics,
            CognitiveReflectionTest,
            End]
