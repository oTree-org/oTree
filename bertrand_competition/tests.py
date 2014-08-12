import otree.test
from otree.common import Money, money_range
import bertrand_competition.views as views
from bertrand_competition.utilities import Bot
import random
from otree.common import money_range


class PlayerBot(Bot):

    def play(self):
        # start
        self.submit(views.Introduction)

        # compete price
        self.submit(views.Compete, {'price': random.choice(money_range(self.treatment.minimum_price+0.01, self.treatment.maximum_price))})

        # results
        self.submit(views.Results)


