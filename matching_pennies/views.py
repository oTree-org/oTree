# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import matching_pennies.forms as forms
from matching_pennies.utilities import ParticipantMixin, ExperimenterMixin
from django.utils.translation import ugettext as _
from django.conf import settings
from ptree.common import currency


class Introduction(ParticipantMixin, ptree.views.Page):

    def show_skip_wait(self):
        return self.PageActions.show

    template_name = 'matching_pennies/Introduction.html'

    def variables_for_template(self):
        return {
            'participant_id': self.participant.index_among_participants_in_match,
            'winner_amount': currency(self.treatment.winner_amount)
        }


class Choice(ParticipantMixin, ptree.views.Page):

    def show_skip_wait(self):
        return self.PageActions.show

    template_name = 'matching_pennies/Choice.html'

    def get_form_class(self):
        return forms.PennySideForm


class Results(ParticipantMixin, ptree.views.Page):

    def show_skip_wait(self):
        if self.participant.other_participant().penny_side:
            return self.PageActions.show
        else:
            return self.PageActions.wait

    template_name = 'matching_pennies/Results.html'

    def variables_for_template(self):
        if self.participant.payoff is None:
            self.participant.set_payoff()

        return {'my_choice': self.participant.penny_side,
                'other_choice': self.participant.other_participant().penny_side,
                'payoff': currency(self.participant.payoff),
                'participant_id': self.participant.index_among_participants_in_match
        }


class ExperimenterPage(ExperimenterMixin, ptree.views.ExperimenterPage):
    pass


def pages():
    return [
        Introduction,
        Choice,
        Results
    ]