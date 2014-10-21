# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils.safestring import mark_safe
from utils import FeedbackQ


def variables_for_all_templates(self):
    return dict(instructions='volunteer_dilemma/Instructions.html')


class Introduction(Page):

    template_name = 'global/Introduction.html'

    def participate_condition(self):
        return self.subsession.round_number == 1


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = 'training_my_payoff',
    question = '''Suppose you and another participant volunteered while \
    the other participant did not. What would be your payoff?'''

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        return dict(question=self.question)


class Feedback1(Page):
    template_name = 'global/Feedback.html'

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        p = self.player
        return dict(
            answer=[p.training_my_payoff, 60],
            explanation=mark_safe(Question1.question + '''
            <strong>Solution:</strong> Your payoff would be 60 points.
            <strong>Explanation:</strong> As at least one (actually 2)\
            participants volunteered, everyone received <strong>100</strong>\
            points. You vonlunteered, so you had to pay <strong>40</strong>\
            points. Together you had <strong>100-40=60</strong> points.'''))


class Decision(Page):

    template_name = 'volunteer_dilemma/Decision.html'

    form_model = models.Player
    form_fields = ['volunteer']

    def variables_for_template(self):
        return {'general_benefit': Constants.general_benefit,
                'volunteer_cost': Constants.volunteer_cost,
                'num_other_players': self.group.players_per_group - 1}


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    template_name = 'volunteer_dilemma/Results.html'

    def variables_for_template(self):
        return {'volunteer': self.player.volunteer,
                'payoff': self.player.payoff,
                'num_volunteers': len([
                    p for p in self.group.get_players() if p.volunteer])}


class FeedbackQ(FeedbackQ, Page):
    form_model = models.Player


def pages():

    return [Introduction,
            Question1,
            Feedback1,
            Decision,
            ResultsWaitPage,
            Results,
            FeedbackQ]
