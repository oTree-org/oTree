from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
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
        self.group.set_payoffs()

class Results(Page):
    def vars_for_template(self):
        pass

page_sequence = [Introduction,
                 ChoiceOne,
                 ChoiceTwoWaitPage,
                 ChoiceTwo,
                 ResultsWaitPage,
                 Results]
