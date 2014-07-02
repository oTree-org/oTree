# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import guessing.forms as forms
from guessing.utilities import ParticipantMixin, ExperimenterMixin
from ptree.common import currency


class Introduction(ParticipantMixin, ptree.views.Page):

    def show_skip_wait(self):
        return self.PageActions.show

    template_name = 'guessing/Introduction.html'


class Guess(ParticipantMixin, ptree.views.Page):

    def show_skip_wait(self):
        return self.PageActions.show

    template_name = 'guessing/Guess.html'

    def get_form_class(self):
        return forms.GuessForm


class Results(ParticipantMixin, ptree.views.Page):

    def show_skip_wait(self):
        if self.participant.payoff is None:
            return self.PageActions.wait
        return self.PageActions.show

    template_name = 'guessing/Results.html'

    def variables_for_template(self):
        return {
            'payoff': self.participant.payoff,
            'guess_value': self.participant.guess_value,
        }


class Experimenter(ExperimenterMixin, ptree.views.ExperimenterPage):

    template_name = 'guessing/Experimenter.html'

    def show_skip_wait(self):
        if any(p.guess_value is None for p in self.subsession.participants()):
            return self.PageActions.wait
        for m in self.subsession.matches():
            m.calculate_average()
            m.save()
        for p in self.subsession.participants():
            p.set_payoff()
            p.save()
        return self.PageActions.show

    def wait_page_title_text(self):
        return "Experimenter"

    def wait_page_body_text(self):
        participant_count = len(self.subsession.participants())
        participant_string = "participants" if participant_count > 1 else "participant"
        return """All {} {} have started playing the game.
                  As the experimenter in this game, you have no particular role to play.
                  This page will change once all participants have been given a
                  payoff.""".format(participant_count, participant_string)

    def variables_for_template(self):
        return {'participant_count': len(self.subsession.participants())}


def experimenter_pages():

    return [Experimenter]


def pages():
    return [
        Introduction,
        Guess,
        Results
    ]