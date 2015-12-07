# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants


def vars_for_all_templates(self):

    return {'total_q': 1,
            'total_rounds': Constants.num_rounds,
            'round_number': self.subsession.round_number}


class Introduction(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1


class Question(Page):

    template_name = 'stag_hunt/Question.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = [
        'training_question_1_my_payoff','training_question_1_other_payoff'
    ]

    def vars_for_template(self):
        return {'num_q': 1}


class Feedback(Page):

    def vars_for_template(self):
        return {
            'num_q': 1,
        }


class Decide(Page):

    def is_displayed(self):
        return True

    form_model = models.Player
    form_fields = ['decision']

    def vars_for_template(self):
        return {'player_index': self.player.id_in_group,
                'stag_stag': Constants.stag_stag_amount,
                'stag_hare': Constants.stag_hare_amount,
                'hare_stag': Constants.hare_stag_amount,
                'hare_hare': Constants.hare_hare_amount}


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()

    body_text = "Waiting for the other participant."


class Results(Page):

    def is_displayed(self):
        return True

    def vars_for_template(self):

        return {
             'total_payoff': self.player.payoff + Constants.fixed_pay}


page_sequence = [Introduction,
            Question,
            Feedback,
            Decide,
            ResultsWaitPage,
            Results]
