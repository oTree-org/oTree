# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import dictator.forms as forms
from dictator.utilities import ParticipantMixIn, MatchMixIn, SubsessionMixIn
from ptree.common import currency


class Introduction(ParticipantMixIn, ptree.views.Page):

    template_name = 'dictator/Introduction.html'

    def variables_for_template(self):
        return {'allocated_amount': currency(self.treatment.allocated_amount),
                'participant_id': self.participant.index_among_participants_in_match}


class Offer(ParticipantMixIn, ptree.views.Page):

    template_name = 'dictator/Offer.html'

    def get_form_class(self):
        return forms.OfferForm

    def participate_condition(self):
        return self.participant.index_among_participants_in_match == 1


class ResultsCheckpoint(MatchMixIn, ptree.views.MatchCheckpoint):

    def action(self):
        for p in self.match.participants():
            p.set_payoff()

    def wait_page_body_text(self):
        if self.participant.index_among_participants_in_match == 2:
            return "Waiting for the dictator to make an offer."


class Results(ParticipantMixIn, ptree.views.Page):

    template_name = 'dictator/Results.html'

    def variables_for_template(self):
        return {'payoff': currency(self.participant.payoff),
                'offer_amount': currency(self.match.offer_amount),
                'participant_id': self.participant.index_among_participants_in_match}


def pages():

    return [Introduction,
            Offer,
            ResultsCheckpoint,
            Results]


