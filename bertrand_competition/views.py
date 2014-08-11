# -*- coding: utf-8 -*-
import bertrand_competition.forms as forms
from bertrand_competition.utilities import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range


class Introduction(Page):

    template_name = 'bertrand_competition/Introduction.html'

    def variables_for_template(self):
        return {
            'minimum_price': self.treatment.minimum_price,
            'maximum_price': self.treatment.maximum_price
        }


class Compete(Page):

    template_name = 'bertrand_competition/Compete.html'

    def get_form_class(self):
        return forms.PriceForm

class ResultsWaitPage(MatchWaitPage):

    def action(self):
        for p in self.match.participants():
            p.set_payoff()

class Results(Page):

    template_name = 'bertrand_competition/Results.html'

    def variables_for_template(self):

        return {
            'payoff': self.participant.payoff,
            'is_winner': self.participant.is_winner,
            'price': self.participant.price,
            'other_price': self.participant.other_participant().price,
            'equal_price': self.participant.price == self.participant.other_participant().price,
        }

def pages():
    return [
        Introduction,
        Compete,
        ResultsWaitPage,
        Results
    ]