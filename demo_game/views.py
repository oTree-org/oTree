# -*- coding: utf-8 -*-
import otree.views
import otree.views.concrete
import demo_game.forms as forms
from demo_game._builtin import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import currency


class Introduction(Page):

    template_name = 'demo_game/Introduction.html'


class FormsDemo(Page):

    template_name = 'demo_game/FormsDemo.html'

    def get_form_class(self):
        return forms.DemoForm


class EmbedDemo(Page):

    template_name = 'demo_game/EmbedDemo.html'


class BootstrapWidgetDemo(Page):

    template_name = 'demo_game/BootstrapWidgetsDemo.html'


class BootstrapWidgetDemo(Page):

    template_name = 'demo_game/BootstrapWidgetsDemo.html'


class AdminDemo(Page):

    template_name = 'demo_game/AdminDemo.html'


class Results(Page):

    def variables_for_template(self):
        if self.player.payoff is None:
            self.player.set_payoff()
        return {
            'payoff': currency(self.player.payoff)
        }

    template_name = 'demo_game/Results.html'


def pages():
    return [
        Introduction,
        EmbedDemo,
        FormsDemo,
        BootstrapWidgetDemo,
        # AdminDemo # need to update this page, provide correct password and link, GIF screenshot, etc
        Results,
    ]