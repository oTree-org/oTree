# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import questionnaire_zurich.forms as forms
from questionnaire_zurich.utilities import ParticipantMixin, ExperimenterMixin
from django.utils.translation import ugettext as _


class Start(ParticipantMixin, ptree.views.Page):

    template_name = 'questionnaire_zurich/Start.html'

    def show_skip_wait(self):
        if all(p.visited for p in self.subsession.participants()):
            return self.PageActions.show
        else:
            return self.PageActions.wait

    def variables_for_template(self):
        if self.participant.payoff is None:
            self.participant.set_payoff()

    def wait_page_body_text(self):
        return _('Waiting for the other participants.')


class Demographics(ParticipantMixin, ptree.views.Page):

    form_class = forms.DemographicsForm
    template_name = 'questionnaire_zurich/Questionnaire.html'


class CognitiveReflectionTestNew(ParticipantMixin, ptree.views.Page):

    form_class = forms.CognitiveReflectionTestNewForm
    template_name = 'questionnaire_zurich/Questionnaire.html'

    def after_valid_form_submission(self):
        self.participant.crt_meal = self.participant.crt_meal_float * 100


class CognitiveReflectionTest(ParticipantMixin, ptree.views.Page):

    form_class = forms.CognitiveReflectionTestForm
    template_name = 'questionnaire_zurich/Questionnaire.html'

    def after_valid_form_submission(self):
        self.participant.crt_bat = self.participant.crt_bat_float * 100


class Results(ParticipantMixin, ptree.views.Page):

    template_name = 'questionnaire_zurich/End.html'

    def variables_for_template(self):
        self.participant.finished_questionnaire = True

def pages():
    return [
        Start,
        Demographics,
        CognitiveReflectionTestNew,
        CognitiveReflectionTest
    ]