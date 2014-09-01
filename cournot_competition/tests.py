import otree.test
from otree.common import Money, money_range
import cournot_competition.views as views
from cournot_competition._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):
        # start
        self.submit(views.Introduction)

        # compete quantity
        self.submit(views.Decide, {'quantity': random.choice(range(1, (self.treatment.total_capacity)/2))})

        # results
        self.submit(views.Results)


