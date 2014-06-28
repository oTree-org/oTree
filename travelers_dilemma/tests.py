import ptree.test
import travelers_dilemma.views as views
from travelers_dilemma.utilities import ParticipantMixin, ExperimenterMixin
import random


class ParticipantBot(ParticipantMixin, ptree.test.ParticipantBot):

    def play(self):

        # basic assertions
        assert (self.treatment.max_value == 100)
        assert (self.treatment.min_value == 20)

        # start game
        self.submit(views.Introduction)

        # player 1: estimate
        if self.participant.index_among_participants_in_match == 1:
            self.play_p1()

        # player 2: estimate
        else:
            self.play_p2()

        self.submit(views.Results)
        print self.participant.payoff

    def play_p1(self):
        self.submit(views.Estimate, {"estimate_value": random.choice(self.match.value_choices())})

    def play_p2(self):
        self.submit(views.Estimate, {"estimate_value": random.choice(self.match.value_choices())})


class ExperimenterBot(ExperimenterMixin, ptree.test.ExperimenterBot):

    def play(self):

        self.submit(views.ExperimenterIntroduction)

