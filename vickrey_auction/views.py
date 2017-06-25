from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    pass


class Bid(Page):
    form_model = models.Player
    form_fields = ['bid_amount']

    def vars_for_template(self):
        return {'endowment_plus_private_value': Constants.endowment + self.player.private_value}


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    pass


page_sequence = [
    Introduction,
    Bid,
    ResultsWaitPage,
    Results]
