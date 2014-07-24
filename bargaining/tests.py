import ptree.test
import bargaining.views as views
from bargaining.utilities import ParticipantMixIn, MatchMixIn, SubsessionMixIn


class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):

        # start
        self.submit(views.Introduction)

        # request
        self.submit(views.Request, {"request_amount": 45})  # figure out how to randomize this amount

        # results
        self.submit(views.Results)


class ExperimenterBot(SubsessionMixIn, ptree.test.ExperimenterBot):

    def play(self):
        pass
