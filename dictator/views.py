# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from utils import FeedbackQ


def variables_for_all_templates(self):
    return {'instructions': 'dictator/Instructions.html',
            'constants': Constants}


class Introduction(Page):

    template_name = 'global/Introduction.html'


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = (
        'training_participant1_payoff', 'training_participant2_payoff')

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        return {'question_template': 'dictator/Question.html'}


class Feedback1(Page):
    template_name = 'dictator/Feedback.html'

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        p = self.player
        return {'answers': {
                'participant 1': [p.training_participant1_payoff, 88],
                'participant 2': [p.training_participant2_payoff, 12]}}


class Offer(Page):

    template_name = 'dictator/Offer.html'

    form_model = models.Group
    form_fields = ['kept']

    def participate_condition(self):
        return self.player.id_in_group == 1


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def body_text(self):
        if self.player.id_in_group == 2:
            return "You are participant 2. \
                Waiting for participant 1 to decide."


class Results(Page):

    template_name = 'dictator/Results.html'

    def variables_for_template(self):
        return {'payoff': self.player.payoff,
                'offer': Constants.allocated_amount - self.group.kept,
                'kept': self.group.kept,
                'player_id': self.player.id_in_group}


class FeedbackQ(FeedbackQ, Page):
    form_model = models.Player


def pages():

    return [Introduction,
            Question1,
            Feedback1,
            Offer,
            ResultsWaitPage,
            Results,
            FeedbackQ]
