# -*- coding: utf-8 -*-
import survey.models as models
from survey._builtin import Page
from otree.common import Money


class Survey(Page):

    template_name = 'survey/Survey.html'

    form_model = models.Player
    form_fields = ['q_gender']


def pages():

    return [Survey]
