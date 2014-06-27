import ptree.test
import public_goods.views as views
from public_goods.utilities import ParticipantMixin, ExperimenterMixin
import random


class ParticipantBot(ParticipantMixin, ptree.test.ParticipantBot):

    def play(self):

        # all players
        self.submit(views.Introduction)

        # each player contributes random amount
        print "Contribution P{}:".format(self.participant.index_among_participants_in_match,)
        self.submit(views.Contribute, {"contributed_amount": random.choice(self.participant.contribute_choices())})

        # submit results page
        self.submit(views.Results)

        # print payoffs
        if self.participant.index_among_participants_in_match == 1:
            for match in self.subsession.matches():
                for player in match.participants():
                    print "Payoff P{} = {}".format(player.index_among_participants_in_match, player.payoff)


class ExperimenterBot(ExperimenterMixin, ptree.test.ExperimenterBot):

    def play(self):

        self.submit(views.ExperimenterPage)
