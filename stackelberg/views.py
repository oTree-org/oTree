# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    pass


class ChoiceOne(Page):
    def is_displayed(self):
        return self.player.id_in_group == 1

    form_model = models.Player
    form_fields = ['quantity']


class ChoiceTwoWaitPage(WaitPage):
    def vars_for_template(self):
        if self.player.id_in_group == 1:
            body_text = "Waiting for the other participant to decide."
        else:
            body_text = 'You are to decide second. Waiting for the other participant to decide first.'
        return {'body_text': body_text}


class ChoiceTwo(Page):
    def is_displayed(self):
        return self.player.id_in_group == 2

    form_model = models.Player
    form_fields = ['quantity']


class ResultsWaitPage(WaitPage):
    body_text = "Waiting for the other participant to decide."

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()


class Results(Page):
    def vars_for_template(self):
        self.player.set_payoff()

        return {
            'total_quantity': self.player.quantity + self.player.other_player().quantity,
            'total_plus_base': self.player.payoff + Constants.fixed_pay
        }


page_sequence = [Introduction,
                 ChoiceOne,
                 ChoiceTwoWaitPage,
                 ChoiceTwo,
                 ResultsWaitPage,
                 Results]
