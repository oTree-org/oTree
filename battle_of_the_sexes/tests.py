import otree.test
from otree.common import Money, money_range
import battle_of_the_sexes.views as views
from battle_of_the_sexes._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # random decision
        choice = random.choice(['football', 'opera'])

        self.submit(views.Decide, {"decision": choice})

        # results
        self.submit(views.Results)
