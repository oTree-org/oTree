from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class Decision(Page):
    form_model = models.Player
    form_fields = ['volunteer']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def vars_for_template(self):
        return {
            'num_volunteers': len([
                                      p for p in self.group.get_players() if
                                      p.volunteer])}


page_sequence = [Introduction,
                 Decision,
                 ResultsWaitPage,
                 Results]
