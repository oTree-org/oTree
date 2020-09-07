# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants
def vars_for_all_templates(self):

    return {'total_capacity': Constants.total_capacity,
            'max_units_per_player': Constants.max_units_per_player,
            'total_q': 1}


class Introduction(Page):

    template_name = 'cournot_competition/Introduction.html'


class Question1(Page):

    template_name = 'cournot_competition/Question.html'

    form_model = models.Player
    form_fields = ['training_question_1']

    def vars_for_template(self):
        return {'num_q': 1}


class Feedback1(Page):

    template_name = 'cournot_competition/Feedback.html'

    def vars_for_template(self):
        return {'num_q': 1}


class Decide(Page):

    form_model = models.Player
    form_fields = ['units']


class ResultsWaitPage(WaitPage):

    body_text = "Waiting for the other participant to decide."

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    def vars_for_template(self):
        return {'total_plus_base': self.player.payoff + Constants.base_points}


page_sequence = [Introduction,
            Question1,
            Feedback1,
            Decide,
            ResultsWaitPage,
            Results]
