# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import dictator.forms as forms
from dictator.utilities import ParticipantMixin, ExperimenterMixin
from ptree.common import currency


class Introduction(ParticipantMixin, ptree.views.Page):

    template_name = 'dictator/Introduction.html'

    def show_skip_wait(self):
        return self.PageActions.show

    def variables_for_template(self):
        return {'allocated_amount': currency(self.treatment.allocated_amount),
                'participant_id': self.participant.index_among_participants_in_match}


class Offer(ParticipantMixin, ptree.views.Page):

    template_name = 'dictator/Offer.html'

    def get_form_class(self):
        return forms.OfferForm

    def show_skip_wait(self):
        if self.participant.index_among_participants_in_match == 1:
            return self.PageActions.show
        else:
            return self.PageActions.skip


class Results(ParticipantMixin, ptree.views.Page):

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


class ExperimenterIntroduction(ExperimenterMixin, ptree.views.ExperimenterPage):

    """This page is only for the experimenter,
    and because the experimenter doesn't have to do anything in this game,
    this page is a waiting screen and is updated once all participants are finished"""

    template_name = 'dictator/Experimenter.html'

    def show_skip_wait(self):
        if all(p.payoff is not None for p in self.subsession.participants()):
            return self.PageActions.show
        else:
            return self.PageActions.wait

    def wait_page_title_text(self):
        return "Dictator Game: Experimenter Page"

    def wait_page_body_text(self):
        participant_count = len(self.subsession.participants())
        participant_string = "participants" if participant_count > 1 else "participant"
        return """All {} {} have started playing the game.
                  As the experimenter in this game, you have no particular role to play.
                  This page will change once all participants have been given a
                  payoff.""".format(participant_count, participant_string)

    def variables_for_template(self):
        return {'participant_count': len(self.subsession.participants())}


def pages():

    return [Introduction,
            Offer,
            Results]


def experimenter_pages():

    return [ExperimenterIntroduction]
