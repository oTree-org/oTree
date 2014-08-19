import otree.test
from otree.common import Money, money_range
import stackelberg_competition.views as views
from stackelberg_competition._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):
        # Start
        self.submit(views.Introduction)

        # player one
        if self.player.index_among_players_in_match == 1:
            self.play_1()

        # player two
        elif self.player.index_among_players_in_match == 2:
            self.play_2()

        # Results
        self.submit(views.Results)

    def play_1(self):
        # Player One: quantity
        self.submit(views.ChoiceOne, {'quantity': random.randint(1, self.treatment.total_capacity/2)})

    def play_2(self):
        # Player two: quantity
        self.submit(views.ChoiceTwo, {'quantity': random.randint(1, self.treatment.total_capacity/2)})


