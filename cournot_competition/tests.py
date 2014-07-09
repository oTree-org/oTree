import ptree.test
import cournot_competition.views as views
from cournot_competition.utilities import ParticipantMixIn, ExperimenterMixIn
import random


class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):
        # start
        self.submit(views.Introduction)

        # compete quantity
        self.submit(views.Compete, {'quantity': random.choice(range(1, (self.treatment.total_capacity)/2))})

        # results
        self.submit(views.Results)


class ExperimenterBot(ExperimenterMixIn, ptree.test.ExperimenterBot):

    def play(self):
        pass
