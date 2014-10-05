# -*- coding: utf-8 -*-
from __future__ import division
import survey_sample.models as models
from survey_sample._builtin import Page
from otree.common import Money


class Survey(Page):

    template_name = 'survey_sample/Survey.html'

    form_model = models.Player
    form_fields = ['q_gender']


def pages():

    return [Survey]
