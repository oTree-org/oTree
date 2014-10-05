# -*- coding: utf-8 -*-
from __future__ import division
import stackelberg_competition.views as views
from stackelberg_competition._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        self.submit(views.Introduction)

        # player one
        if self.player.index_among_players_in_match == 1:
            self.play_1()

        # player two
        elif self.player.index_among_players_in_match == 2:
            self.play_2()

        self.submit(views.Results)

    def play_1(self):
        self.submit(views.ChoiceOne, {'quantity': random.randint(0, self.subsession.max_units_per_player())})

    def play_2(self):
        self.submit(views.ChoiceTwo, {'quantity': random.randint(0, self.subsession.max_units_per_player())})
