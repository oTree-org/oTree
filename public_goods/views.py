# -*- coding: utf-8 -*-
import public_goods.forms as forms
from public_goods.utilities import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range

def variables_for_all_templates(self):
    return {'amount_allocated': self.treatment.amount_allocated}

class Introduction(Page):

    """Description of the game: How to play and returns expected"""

    template_name = 'public_goods/Introduction.html'

    def variables_for_template(self):
        return {'no_of_participants': self.match.participants_per_match,
                'multiplication_factor': self.treatment.multiplication_factor}


class Contribute(Page):

    """Participant: Choose how much to contribute"""

    template_name = 'public_goods/Contribute.html'

    def get_form_class(self):
        return forms.ContributeForm


class ResultsWaitPage(MatchWaitPage):

    def action(self):
        self.match.set_contributions()
        self.match.set_individual_share()
        for p in self.match.participants():
            p.set_payoff()

    def body_text(self):
        return "Waiting for other group members to contribute."


class Results(Page):

    """Participants payoff: How much each has earned"""

    template_name = 'public_goods/Results.html'

    def variables_for_template(self):

        participants = self.match.participants()

        return {
            'contributed_amount': self.participant.contributed_amount,
            'participants': participants,
            'id': self.participant.index_among_participants_in_match
        }


def pages():

    return [Introduction,
            Contribute,
            ResultsWaitPage,
            Results]
