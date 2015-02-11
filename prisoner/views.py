# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

def vars_for_all_templates(self):

    return {
             'total_q': 1,
        }


class Introduction(Page):

    template_name = 'prisoner/Introduction.html'

    timeout_seconds = 100


class Question1(Page):

    template_name = 'prisoner/Question.html'

    form_model = models.Player
    form_fields = ['training_question_1']

    def vars_for_template(self):
        return {'num_q': 1}

    timeout_seconds = 100

class Feedback1(Page):

    template_name = 'prisoner/Feedback.html'

    def vars_for_template(self):
        return {'num_q': 1,
                'question': 'Suppose Alice chose to defect and Bob chose to cooperate. How many points would Alice and Bob receive, respectively?',
                }

class Decision(Page):

    template_name = 'prisoner/Decision.html'

    form_model = models.Player
    form_fields = ['decision']



class ResultsWaitPage(WaitPage):



    def body_text(self):
        return 'Waiting for the other participant to choose.'

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()


class Results(Page):

    template_name = 'prisoner/Results.html'

    def vars_for_template(self):


        self.player.set_payoff()

        return {
            'my_decision': self.player.decision.lower(),
            'other_player_decision': self.player.other_player().decision.lower(),
            'same_choice': self.player.decision == self.player.other_player().decision,
            'total_plus_base': self.player.payoff + Constants.base_points
        }



def pages():

    return [
        Introduction,
        Question1,
        Feedback1,
        Decision,
        ResultsWaitPage,
        Results
    ]
