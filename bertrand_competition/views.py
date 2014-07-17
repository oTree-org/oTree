# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import bertrand_competition.forms as forms
from bertrand_competition.utilities import ParticipantMixIn, ExperimenterMixIn
from ptree.common import currency


class Introduction(ParticipantMixIn, ptree.views.Page):

    def show_skip_wait(self):
        return self.PageActions.show

    template_name = 'bertrand_competition/Introduction.html'

    def variables_for_template(self):
        return {
            'minimum_price': currency(self.treatment.minimum_price),
            'maximum_price': currency(self.treatment.maximum_price)
        }


class Compete(ParticipantMixIn, ptree.views.Page):

    def show_skip_wait(self):
        return self.PageActions.show

    template_name = 'bertrand_competition/Compete.html'

    def get_form_class(self):
        return forms.PriceForm


class Results(ParticipantMixIn, ptree.views.Page):

    def show_skip_wait(self):
        if self.participant.other_participant().price:
            return self.PageActions.show
        else:
            return self.PageActions.wait

    template_name = 'bertrand_competition/Results.html'

    def variables_for_template(self):
        if self.participant.payoff is None:
            self.participant.set_payoff()

        return {
            'payoff': currency(self.participant.payoff),
            'is_winner': self.participant.is_winner,
            'price': currency(self.participant.price),
            'other_price': currency(self.participant.other_participant().price),
            'equal_price': True if self.participant.price == self.participant.other_participant().price else False,
        }


class ExperimenterPage(ExperimenterMixIn, ptree.views.ExperimenterPage):
    pass


def pages():
    return [
        Introduction,
        Compete,
        Results
    ]