from otree.api import Currency as c, currency_range, expect
from . import app
from otree.api import Bot
from .app import Constants


class PlayerBot(Bot):
    def play_round(self):

        yield app.Introduction

        if self.player.id_in_group == 1:
            yield app.Send, dict(sent_amount=4)

        else:
            yield app.SendBack, dict(sent_back_amount=8)

        yield app.Results
