# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import survey.forms as forms
from survey.utilities import ParticipantMixin, ExperimenterMixin


class Start(ParticipantMixin, ptree.views.Page):

    template_name = 'survey/Start.html'

    def show_skip_wait(self):
        if all(p.visited for p in self.subsession.participants()):
            return self.PageActions.show
        else:
            return self.PageActions.wait

    def variables_for_template(self):
        if self.participant.payoff is None:
            self.participant.set_payoff()

    def wait_page_body_text(self):
        return "Waiting for the other participants."


class Demographics(ParticipantMixin, ptree.views.Page):

    form_class = forms.DemographicsForm
    template_name = 'survey/Survey.html'


class CognitiveReflectionTest(ParticipantMixin, ptree.views.Page):

    form_class = forms.CognitiveReflectionTestForm
    template_name = 'survey/Survey.html'

    def after_valid_form_submission(self):
        self.participant.crt_bat = self.participant.crt_bat_float * 100


class End(ParticipantMixin, ptree.views.Page):

    template_name = 'survey/End.html'


def pages():

    return [Start,
            Demographics,
            CognitiveReflectionTest,
            End]
