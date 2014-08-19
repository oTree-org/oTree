# -*- coding: utf-8 -*-
import public_goods.forms as forms
from public_goods._builtin import Page, MatchWaitPage


def variables_for_all_templates(self):
    return {'amount_allocated': self.treatment.amount_allocated}


class Introduction(Page):

    """Description of the game: How to play and returns expected"""

    template_name = 'public_goods/Introduction.html'

    def variables_for_template(self):
        return {'no_of_players': self.match.players_per_match,
                'multiplication_factor': self.treatment.multiplication_factor}


class Contribute(Page):

    """Player: Choose how much to contribute"""

    template_name = 'public_goods/Contribute.html'

    def get_form_class(self):
        return forms.ContributeForm


class ResultsWaitPage(MatchWaitPage):

    def after_all_players_arrive(self):
        self.match.set_payoffs()

    def body_text(self):
        return "Waiting for other group members to contribute."


class Results(Page):

    """Players payoff: How much each has earned"""

    template_name = 'public_goods/Results.html'

    def variables_for_template(self):

        players = self.match.players

        return {
            'contribution': self.player.contribution,
            'players': players,
            'id': self.player.index_among_players_in_match
        }


def pages():

    return [Introduction,
            Contribute,
            ResultsWaitPage,
            Results]
