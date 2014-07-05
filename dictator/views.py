# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import dictator.forms as forms
from dictator.utilities import ParticipantMixIn, ExperimenterMixIn
from ptree.common import currency


class Introduction(ParticipantMixIn, ptree.views.Page):

    template_name = 'dictator/Introduction.html'

    def show_skip_wait(self):
        return self.PageActions.show

    def variables_for_template(self):
        return {'allocated_amount': currency(self.treatment.allocated_amount),
                'participant_id': self.participant.index_among_participants_in_match}


class Offer(ParticipantMixIn, ptree.views.Page):

    template_name = 'dictator/Offer.html'

    def get_form_class(self):
        return forms.OfferForm

    def show_skip_wait(self):
        if self.participant.index_among_participants_in_match == 1:
            return self.PageActions.show
        else:
            return self.PageActions.skip


class Results(ParticipantMixIn, ptree.views.Page):

    template_name = 'dictator/Results.html'

    def show_skip_wait(self):
        if self.match.offer_amount is None:
            return self.PageActions.wait
        else:
            return self.PageActions.show

    def wait_page_body_text(self):
        if self.participant.index_among_participants_in_match == 2:
            return "Waiting for the dictator to make an offer."

    def variables_for_template(self):
        if self.participant.payoff is None:
            self.participant.set_payoff()

        return {'payoff': currency(self.participant.payoff),
                'offer_amount': currency(self.match.offer_amount),
                'participant_id': self.participant.index_among_participants_in_match}


def pages():

    return [Introduction,
            Offer,
            Results]


