# -*- coding: utf-8 -*-
import tragedy_of_the_commons.models as models
from tragedy_of_the_commons._builtin import Page, WaitPage
from otree.common import Money, money_range


class Introduction(Page):

    def participate_condition(self):
        return True

    template_name = 'tragedy_of_the_commons/Introduction.html'

    def variables_for_template(self):

        return {'common_gain': self.treatment.common_gain,
                'common_loss': self.treatment.common_loss,
                'common_cost': self.treatment.individual_gain - self.treatment.defect_costs,
                'defect_gain': self.treatment.common_gain - self.treatment.defect_costs}


class Decision(Page):

    def participate_condition(self):
        return True

    template_name = 'tragedy_of_the_commons/Decision.html'

    form_model = models.Player
    form_fields = ['decision']


class ResultsWaitPage(WaitPage):

    group = models.Match

    def after_all_players_arrive(self):
        self.match.set_payoffs()


class Results(Page):

    template_name = 'tragedy_of_the_commons/Results.html'

    def variables_for_template(self):
        return {'payoff': self.player.payoff}


def pages():

    return [Introduction,
            Decision,
            ResultsWaitPage,
            Results]
