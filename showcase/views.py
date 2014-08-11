# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import showcase.forms as forms
from showcase.utilities import Page, MatchWaitPage, SubsessionWaitPage
from ptree.common import currency


class Introduction(Page):

    template_name = 'showcase/Introduction.html'


class FormsDemo(Page):

    template_name = 'showcase/FormsDemo.html'

    def get_form_class(self):
        return forms.DemoForm


class EmbedDemo(Page):

    template_name = 'showcase/EmbedDemo.html'


class BootstrapWidgetDemo(Page):

    template_name = 'showcase/BootstrapWidgetsDemo.html'


class BootstrapWidgetDemo(Page):

    template_name = 'showcase/BootstrapWidgetsDemo.html'


class AdminDemo(Page):

    template_name = 'showcase/AdminDemo.html'


class Results(Page):

    def variables_for_template(self):
        if self.participant.payoff is None:
            self.participant.set_payoff()
        return {
            'payoff': currency(self.participant.payoff)
        }

    template_name = 'showcase/Results.html'


def pages():
    return [
        Introduction,
        FormsDemo,
        EmbedDemo,
        BootstrapWidgetDemo,
        AdminDemo,
        Results,
    ]