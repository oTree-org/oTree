import ptree.test
import matching_pennies.views as views
from matching_pennies.utilities import ParticipantMixIn, ExperimenterMixIn
import random


class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):

        # both players choose their heads or tails
        choice = random.choice(self.participant.PENNY_CHOICES)[0]
        if self.participant.index_among_participants_in_match == 1:
            self.submit(views.Choice, {"penny_side": choice})
        else:
            self.submit(views.Choice, {"penny_side": choice})

        # results after choices
        self.submit(views.Results)



class ExperimenterBot(ExperimenterMixIn, ptree.test.ExperimenterBot):

    def play(self):
        print '**************************'
        print 'Round number: {}'.format(self.subsession.round_number)
