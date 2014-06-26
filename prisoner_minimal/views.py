# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import prisoner_minimal.forms as forms
from prisoner_minimal.utilities import ParticipantMixin, ExperimenterMixin
from django.utils.translation import ugettext as _
from django.conf import settings
from ptree.common import currency


class Decision(ParticipantMixin, ptree.views.Page):

    template_name = 'prisoner_minimal/Decision.html'

    def variables_for_template(self):
        return {'friends_amount': currency(self.treatment.friends_amount),
                'betrayed_amount': currency(self.treatment.betrayed_amount),
                'enemies_amount': currency(self.treatment.enemies_amount),
                'betray_amount': currency(self.treatment.betray_amount)}

    def get_form_class(self):
        return forms.DecisionForm


class Results(ParticipantMixin, ptree.views.Page):

    template_name = 'prisoner_minimal/Results.html'

    def variables_for_template(self):
        if self.participant.payoff is None:
            self.participant.set_payoff()

        return {'my_payoff': currency(self.participant.payoff),
                'my_decision': self.participant.decision.lower(),
                'other_participant_decision': self.participant.other_participant().decision.lower(),
                'same_choice': True if self.participant.decision == self.participant.other_participant().decision else False}

    def show_skip_wait(self):
        if self.participant.other_participant().decision:
            return self.PageActions.show
        else:
            return self.PageActions.wait

    def wait_page_body_text(self):
        return 'Waiting for the other participant to make a decision.'


class ExperimenterIntroduction(ExperimenterMixin, ptree.views.ExperimenterPage):

    template_name = 'prisoner_minimal/ExperimenterPage.html'

    def show_skip_wait(self):
        if all(p.payoff is not None for p in self.subsession.participants()):
            return self.PageActions.show
        else:
            return self.PageActions.wait

    def wait_page_title_text(self):
        return _("Prisoner's Dilemma: Experimenter Page")

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

    return [Decision,
            Results]


def experimenter_pages():

    return [ExperimenterIntroduction]
