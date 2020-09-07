from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Send(Page):

    form_model = 'group'
    form_fields = ['sent_amount']

    def is_displayed(self):
        return self.player.id_in_group == 1


class WaitForP1(WaitPage):
    pass


class SendBack(Page):

    form_model = 'group'
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        return dict(tripled_amount=self.group.sent_amount * Constants.multiplier)


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    pass


page_sequence = [Send, WaitForP1, SendBack, ResultsWaitPage, Results]
