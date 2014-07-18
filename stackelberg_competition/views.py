# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import stackelberg_competition.forms as forms
from stackelberg_competition.utilities import ParticipantMixIn, ExperimenterMixIn
from ptree.common import currency


class Introduction(ParticipantMixIn, ptree.views.Page):

    def show_skip_wait(self):
        return self.PageActions.show

    template_name = 'stackelberg_competition/Introduction.html'

    def variables_for_template(self):
        return {
            'total_capacity': self.treatment.total_capacity
        }


class ChoiceOne(ParticipantMixIn, ptree.views.Page):

    def show_skip_wait(self):
        if self.participant.index_among_participants_in_match == 1:
            return self.PageActions.show
        else:
            return self.PageActions.skip

    template_name = 'stackelberg_competition/ChoiceOne.html'

    def get_form_class(self):
        return forms.QuantityForm


class ChoiceTwo(ParticipantMixIn, ptree.views.Page):

    def show_skip_wait(self):
        if self.participant.index_among_participants_in_match == 2:
            if self.participant.other_participant().quantity is None:
                return self.PageActions.wait
            else:
                return self.PageActions.show
        else:
            return self.PageActions.skip

    template_name = 'stackelberg_competition/ChoiceTwo.html'

    def get_form_class(self):
        return forms.QuantityForm

    def variables_for_template(self):
        return {
            'other_quantity': self.participant.other_participant().quantity
        }


class Results(ParticipantMixIn, ptree.views.Page):

    def show_skip_wait(self):
        if self.participant.other_participant().quantity:
            return self.PageActions.show
        else:
            return self.PageActions.wait

    template_name = 'stackelberg_competition/Results.html'

    def variables_for_template(self):
        if self.participant.payoff is None:
            self.participant.set_payoff()

        return {
            'payoff': currency(self.participant.payoff),
            'quantity': self.participant.quantity,
            'other_quantity': self.participant.other_participant().quantity,
            'price': currency(self.match.price)
        }


class ExperimenterPage(ExperimenterMixIn, ptree.views.ExperimenterPage):
    pass


def pages():
    return [
        Introduction,
        ChoiceOne,
        ChoiceTwo,
        Results
    ]