# -*- coding: utf-8 -*-
import trust.forms as forms
from trust.utilities import Page, MatchWaitPage, SubsessionWaitPage

class Introduction(Page):

    template_name = 'trust/Introduction.html'

    def variables_for_template(self):
        return {'amount_allocated': self.treatment.amount_allocated}


class Send(Page):

    """This page is only for participant one
    P1 sends some (all, some, or none) amount to P2
    This amount is tripled by experimenter, i.e if sent amount by P1 is 10, amount received by P2 is 30"""

    template_name = 'trust/Send.html'

    def get_form_class(self):
        return forms.SendForm

    def participate_condition(self):
        return self.participant.index_among_participants_in_match == 1

    def variables_for_template(self):
        return {'amount_allocated': self.treatment.amount_allocated}


class SimpleWaitPage(MatchWaitPage):

    def body_text(self):
        return 'The other participant has been given the opportunity to give money first. Please wait.'


class SendBack(Page):

    """This page is only for participant two
    P2 sends back some amount (of the tripled amount received) to P1 ranging from 0 to MAX they got"""

    template_name = 'trust/SendBack.html'

    def get_form_class(self):
        return forms.SendBackForm

    def participate_condition(self):
        return self.participant.index_among_participants_in_match == 2

    def variables_for_template(self):
        tripled_amount = self.match.sent_amount * 3
        total_amount = self.treatment.amount_allocated + tripled_amount

        return {'amount_allocated': self.treatment.amount_allocated,
                'sent_amount': self.match.sent_amount,
                'tripled_amount': tripled_amount,
                'total_amount': total_amount}


class ResultsWaitPage(MatchWaitPage):

    def wait_page_body_text(self):
        return 'Waiting for the other participant to finish.'

    def action(self):
        for p in self.match.participants():
            p.set_payoff()


class Results(Page):

    """This page displays the earnings of each participant"""

    template_name = 'trust/Results.html'

    def variables_for_template(self):

        participant1_payoff = self.match.get_payoff_participant_1()
        participant2_payoff = self.match.get_payoff_participant_2()

        tripled_amount = self.match.sent_amount * 3

        return {'amount_allocated': self.treatment.amount_allocated,
                'sent_amount': self.match.sent_amount,
                'tripled_amount': tripled_amount,
                'sent_back_amount': self.match.sent_back_amount,
                'participant_index': self.participant.index_among_participants_in_match,
                'participant1_payoff': participant1_payoff,
                'participant2_payoff': participant2_payoff}


def pages():

    return [Introduction,
            Send,
            SimpleWaitPage,
            SendBack,
            ResultsWaitPage,
            Results]