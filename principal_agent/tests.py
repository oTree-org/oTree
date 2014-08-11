import otree.test
from otree.common import Money, money_range
import principal_agent.views as views
from principal_agent.utilities import Bot


class ParticipantBot(Bot):

    def play(self):
        # intro
        self.submit(views.Introduction)

        if self.participant.index_among_participants_in_match == 1:
            self.play_1()

        else:
            self.play_2()

        # results
        self.submit(views.Results)

    def play_1(self):
        # P1 - offer
        self.submit(views.Offer,
                    {'agent_fixed_pay': 550,
                    'agent_return_share': 40})

    def play_2(self):
        # P2 - accept/reject
        self.submit(views.Accept, {'decision': 'Reject'})


class ExperimenterBot(ExperimenterMixIn, otree.test.ExperimenterBot):

    def play(self):
        pass
