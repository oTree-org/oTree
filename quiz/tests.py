from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        submitted_answer = self.player.current_question()['choice1']
        yield (views.Question, {'submitted_answer': submitted_answer})
        if self.subsession.round_number == Constants.num_rounds:
            yield (views.Results)
