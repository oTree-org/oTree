from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    pass


class Guess(Page):
    form_model = models.Player
    form_fields = ['guess_value']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "Waiting for the other participants."


class Results(Page):
    def vars_for_template(self):
        other_guesses = []
        winners_cnt = int(self.player.is_winner)
        for p in self.player.get_others_in_group():
            other_guesses.append(p.guess_value)
            winners_cnt += int(p.is_winner)

        return {
            'other_guesses': other_guesses,
            'other_guesses_count': len(other_guesses),
            'two_third_average': round(self.group.two_third_guesses, 4),
            'winners_cnt': winners_cnt,
        }


page_sequence = [Introduction,
                 Guess,
                 ResultsWaitPage,
                 Results]
