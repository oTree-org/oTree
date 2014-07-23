import ptree.test
import public_goods.views as views
from public_goods.utilities import ParticipantMixIn, MatchMixIn, SubsessionMixIn
import random


class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):

        # all players
        self.submit(views.Introduction)

        # each player contributes random amount
        self.submit(views.Contribute, {"contributed_amount": random.choice(self.participant.contribute_choices())})

        # submit results page
        self.submit(views.Results)


class ExperimenterBot(SubsessionMixIn, ptree.test.ExperimenterBot):

    def play(self):

        self.submit(views.ExperimenterPage)
