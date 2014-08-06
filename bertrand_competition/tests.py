import ptree.test
from ptree.common import Money, money_range
import bertrand_competition.views as views
from bertrand_competition.utilities import Bot
import random
from ptree.common import money_range


class ParticipantBot(Bot):

    def play(self):
        # start
        self.submit(views.Introduction)

        # compete price
        self.submit(views.Compete, {'price': random.choice(money_range(self.treatment.minimum_price+0.01, self.treatment.maximum_price))})

        # results
        self.submit(views.Results)


