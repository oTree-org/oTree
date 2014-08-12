
import public_goods.views as views
from public_goods.utilities import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # all players
        self.submit(views.Introduction)

        # each player contributes random amount
        self.submit(views.Contribute, {"contribution": random.choice(self.player.contribute_choices())})

        # submit results page
        self.submit(views.Results)
