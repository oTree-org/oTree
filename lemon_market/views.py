from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class Production(Page):
    def is_displayed(self):
        return self.player.role() != 'buyer'

    form_model = models.Player
    form_fields = ['seller_proposed_price', 'seller_proposed_quality']


class SimpleWaitPage(WaitPage):
    pass


class Purchase(Page):
    def is_displayed(self):
        return self.player.role() == 'buyer'

    form_model = models.Group
    form_fields = ['seller_id']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoff()


class Results(Page):
    def vars_for_template(self):
        return {'seller': self.group.get_seller()}


class FinalResults(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        return self.subsession.vars_for_admin_report()




page_sequence = [
    Introduction,
    Production,
    SimpleWaitPage,
    Purchase,
    ResultsWaitPage,
    Results,
    FinalResults,
]
