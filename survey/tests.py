from otree.api import Currency as c, currency_range, expect

from . import app
from otree.api import Bot
from .app import Constants


class PlayerBot(Bot):
    def play_round(self):

        yield app.Demographics, dict(age=24, gender='Male')

        yield (
            app.CognitiveReflectionTest,
            dict(crt_bat=10, crt_widget=5, crt_lake=48),
        )

        for value in [self.player.crt_bat, self.player.payoff]:
            expect(value, '!=', None)
