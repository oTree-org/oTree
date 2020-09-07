# -*- coding: utf-8 -*-
from __future__ import division, absolute_import
from . import models
from otree.api import WaitPage
from tests.utils import BlankTemplatePage as Page


class ErrorMessage(Page):

    form_model = models.Player
    form_fields = ['add100_1', 'add100_2']

    def is_displayed(self):
        return True

    def vars_for_template(self):
        assert self.session.vars['a'] == 1
        assert self.participant.vars['a'] == 1
        assert self.participant.vars['b'] == 1
        assert self.session.config['treatment'] == 'blue'
        assert self.player.in_before_session_starts == 1
        assert self.group.in_before_session_starts == 1

        return {
            'my_variable_here': 1,
        }

    def error_message(self, values):
        if values['add100_1'] + values['add100_2'] != 100:
            return 'The numbers must add up to 100'

    def before_next_page(self):
        self.player.after_next_button_field = True
        self.session.vars['a'] = 2


class FieldErrorMessage(Page):

    form_model = models.Player
    form_fields = ['even_int']

    def even_int_error_message(self, value):
        if value % 2:
            return 'Must be an even number'

    def is_displayed(self):
        # make sure it's available during pre-fetch
        assert self.session
        return True


class DynamicChoices(Page):

    form_model = models.Player

    def get_form_fields(self):
        return ['dynamic_choices']

    def dynamic_choices_choices(self):
        return [
            ['a', 'first choice'],
            ['b', 'second choice'],
        ]


class MinMax(Page):

    form_model = models.Group
    form_fields = ['min_max']


class DynamicMinMax(Page):

    form_model = models.Player
    form_fields = ['dynamic_min_max']

    def dynamic_min_max_min(self):
        return 3

    def dynamic_min_max_max(self):
        return 3


class Blank(Page):
    form_model = models.Player
    form_fields = ['blank']


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        assert self.session.vars['a'] == 2
        self.group.set_payoffs()
        for player in self.group.get_players():
            player.participant.vars['a'] = 2


class Results(Page):

    def vars_for_template(self):
        assert self.player.after_next_button_field is True
        assert self.player.participant.vars['a'] == 2
        participant = self.player.participant
        assert participant.payoff == 50
        assert participant.money_to_pay() == 50 + 9.99
        return {}


page_sequence = [
    ErrorMessage,
    FieldErrorMessage,
    DynamicChoices,
    MinMax,
    DynamicMinMax,
    Blank,
    ResultsWaitPage,
    Results
]
