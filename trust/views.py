# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import trust.forms as forms
from trust.utilities import ParticipantMixin, ExperimenterMixin
from django.utils.translation import ugettext as _
from django.conf import settings
from ptree.common import currency


class Introduction(ParticipantMixin, ptree.views.Page):

    template_name = 'trust/Introduction.html'

    def variables_for_template(self):
        return {'amount_allocated': currency(self.treatment.amount_allocated)}


class Send(ParticipantMixin, ptree.views.Page):
    """This page is only for participant one
      P1 sends some(all, some or none) amount to P2
      This amount is trippled by experimenter i.e if sent amount by P1=10, amount received by P2=30"""
    template_name = 'trust/Send.html'

    def get_form_class(self):
        return forms.SendForm

    def show_skip_wait(self):
        if self.participant.index_among_participants_in_match == 1:
            return self.PageActions.show
        else:
            return self.PageActions.skip

    def variables_for_template(self):
        return {'amount_allocated': currency(self.treatment.amount_allocated)}


class SendBack(ParticipantMixin, ptree.views.Page):
    """This page is only for participant two
      P2 sends back some amount(of the tripled amount received) to P1 ranging from zero to max they got"""
    template_name = 'trust/SendBack.html'

    def get_form_class(self):
        return forms.SendBackForm

    def show_skip_wait(self):
        if self.participant.index_among_participants_in_match == 2:
            if self.match.sent_amount is None:
                return self.PageActions.wait
            else:
                return self.PageActions.show
        else:
            return self.PageActions.skip

    def wait_page_body_text(self):
        return 'The other participant has been given the opportunity to give money first. Please wait.'

    def variables_for_template(self):
        tripled_amount = self.match.sent_amount * 3
        total_amount = self.treatment.amount_allocated + tripled_amount

        return {'amount_allocated': currency(self.treatment.amount_allocated),
                'sent_amount': currency(self.match.sent_amount),
                'tripled_amount': currency(tripled_amount),
                'total_amount': currency(total_amount)}


class Results(ParticipantMixin, ptree.views.Page):
    # How much each Participant has got..
    template_name = 'trust/Results.html'

    def show_skip_wait(self):
        if self.match.sent_amount is not None and self.match.sent_back_amount is not None:
            return self.PageActions.show
        else:
            return self.PageActions.wait

    def wait_page_body_text(self):
        return 'Waiting for the other participant to finish.'

    def variables_for_template(self):
        if self.participant.payoff is None:
            self.participant.set_payoff()

        # get payoffs
        participant1_payoff = self.match.get_payoff_participant_1()
        participant2_payoff = self.match.get_payoff_participant_2()

        tripled_amount = self.match.sent_amount * 3

        return {'amount_allocated': currency(self.treatment.amount_allocated),
                'sent_amount': currency(self.match.sent_amount),
                'tripled_amount': currency(tripled_amount),
                'sent_back_amount': currency(self.match.sent_back_amount),
                'participant_index': self.participant.index_among_participants_in_match,
                'participant1_payoff': currency(participant1_payoff),
                'participant2_payoff': currency(participant2_payoff)}


class ExperimenterIntroduction(ExperimenterMixin, ptree.views.ExperimenterPage):

    template_name = 'trust/ExperimenterPage.html'

    def show_skip_wait(self):
        if all(p.payoff is not None for p in self.subsession.participants()):
            return self.PageActions.show
        else:
            return self.PageActions.wait

    def wait_page_title_text(self):
        return _('Trust Game: Experimenter Page')

    def wait_page_body_text(self):
        participant_count = len(self.subsession.participants())
        participant_string = "participants" if participant_count > 1 else "participant"
        matches_count = len(self.subsession.matches())
        matches_string = "matches" if matches_count > 1 else "match"
        return """All {} {} in {} {} have started playing the game.
                  As the experimenter in this game, you have no particular role to play.
                  This page will change once all participants have been given a
                  payoff.""".format(participant_count, participant_string, matches_count, matches_string)

    def variables_for_template(self):
        return {'participant_count': len(self.subsession.participants())}


def pages():

    return [Introduction,
            Send,
            SendBack,
            Results]


def experimenter_pages():

    return [ExperimenterIntroduction]
