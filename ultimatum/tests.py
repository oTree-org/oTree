import otree.test
import ultimatum.views as views
from ultimatum.utilities import PlayerMixin, ExperimenterMixin
import random


class PlayerBot(PlayerMixin, otree.test.PlayerBot):

    def play(self):

        # both players
        self.submit(views.Introduction)

        # player one
        if self.player.index_among_players_in_match == 1:
            self.play_p1()

        # player two
        elif self.player.index_among_players_in_match == 2:
            self.play_p2()

        # both players
        self.submit(views.Results)

        # both players
        #self.submit(views.Feedback, {'feedback': 'Nice game, maybe offer more rounds...'})

        # print payoff
        print "Player {} payoff: {}".format(self.player.index_among_players_in_match, self.player.payoff)

    def play_p1(self):

        # player one

        # randomly choose an amount to offer from valid offers
        amount_offered = random.choice(self.treatment.offer_choices())
        self.submit(views.Offer, {'amount_offered': amount_offered})

        print self.player.payoff

    def play_p2(self):

        # player two

        # direct response
        if not self.treatment.strategy:

            print "Direct Method"
            if self.treatment.hypothetical:
                print "with Hypothetical"

            self.submit(views.Accept, {'offer_accepted': True})

            # direct response with hypothetical part
            if self.treatment.hypothetical:

                # randomly accept/reject offered amounts
                choices = {}
                for i in range(1, len(self.treatment.offer_choices()) + 1):
                    choices['offer_{}'.format(i)] = random.choice([True, False])

                self.submit(
                    views.AcceptHypothetical, choices
                )

        # strategy method
        elif self.treatment.strategy:

            print "Strategy Method"

            # randomly accept/reject offered amounts
            choices = {}
            for i in range(1, len(self.treatment.offer_choices()) + 1):
                choices['offer_{}'.format(i)] = random.choice([True, False])

            self.submit(
                views.AcceptStrategy, choices
            )


class ExperimenterBot(ExperimenterMixin, otree.test.ExperimenterBot):

    def play(self):

        pass
