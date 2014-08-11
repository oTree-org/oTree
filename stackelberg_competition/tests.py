import otree.test
from otree.common import Money, money_range
import stackelberg_competition.views as views
from stackelberg_competition.utilities import Bot
import random


class ParticipantBot(Bot):

    def play(self):
        # Start
        self.submit(views.Introduction)

        # participant one
        if self.participant.index_among_participants_in_match == 1:
            self.play_1()

        # participant two
        elif self.participant.index_among_participants_in_match == 2:
            self.play_2()

        # Results
        self.submit(views.Results)

    def play_1(self):
        # Participant One: quantity
        self.submit(views.ChoiceOne, {'quantity': random.choice(range(1, (self.treatment.total_capacity)/2))})

    def play_2(self):
        # Participant two: quantity
        self.submit(views.ChoiceTwo, {'quantity': random.choice(range(1, (self.treatment.total_capacity)/2))})


