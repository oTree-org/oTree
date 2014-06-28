# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import travelers_dilemma.forms as forms
from travelers_dilemma.utilities import ParticipantMixin, ExperimenterMixin
from django.utils.translation import ugettext as _
from django.conf import settings
from ptree.common import currency


class Introduction(ParticipantMixin, ptree.views.Page):

    def show_skip_wait(self):
        return self.PageActions.show

    template_name = 'travelers_dilemma/Introduction.html'

    def variables_for_template(self):
        return {
            'max_value': currency(self.treatment.max_value),
            'min_value': currency(self.treatment.min_value),
            'honesty_gain': currency(self.treatment.honesty_gain)
        }


class Estimate(ParticipantMixin, ptree.views.Page):

    def show_skip_wait(self):
        return self.PageActions.show

    template_name = 'travelers_dilemma/Estimate.html'

    def get_form_class(self):
        return forms.EstimateValueForm


class Results(ParticipantMixin, ptree.views.Page):

    def show_skip_wait(self):
        if self.participant.other_participant().estimate_value:
            return self.PageActions.show
        else:
            return self.PageActions.wait

    template_name = 'travelers_dilemma/Results.html'

    def variables_for_template(self):
        if self.participant.payoff is None:
            self.participant.set_payoff()
        return {
            'estimated_value': currency(self.participant.estimate_value),
            'other_estimated_value': currency(self.participant.other_participant().estimate_value),
            'payoff': currency(self.participant.payoff)
        }


class ExperimenterIntroduction(ExperimenterMixin, ptree.views.ExperimenterPage):
    """This page is only for the experimenter,
    and because the experimenter doesn't have to do anything in this game,
    this page is a waiting screen and is updated once all participants are finished"""

    template_name = 'travelers_dilemma/Experimenter.html'

    def show_skip_wait(self):
        if all(p.payoff is not None for p in self.subsession.participants()):
            return self.PageActions.show
        else:
            return self.PageActions.wait

    def wait_page_title_text(self):
        return "Traveler's Dilemma: Experimenter Page"

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
    return [
        Introduction,
        Estimate,
        Results
    ]


def experimenter_pages():
    return [ExperimenterIntroduction]