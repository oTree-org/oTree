from otree.api import Currency as c, currency_range, expect, Bot
from . import *


class PlayerBot(Bot):
    def play_round(self):

        yield Introduction

        if self.player.id_in_group == 1:
            yield Send, dict(sent_amount=4)

        else:
            yield SendBack, dict(sent_back_amount=8)

        yield Results
