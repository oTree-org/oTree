import lying.models as models

class ParticipantMixIn(object):
    z_models = models

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.treatment = models.Treatment()
        self.match = models.Match()
        self.participant = models.Participant()


class SubsessionMixIn(object):

    z_models = models

    def z_autocomplete(self):
        self.subsession = models.Subsession()

class MatchMixIn(object):

    z_models = models

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.treatment = models.Treatment()
        self.match = models.Match()
import ptree.views
class InitializeParticipant(ParticipantMixIn, ptree.views.InitializeParticipant):
    pass
class InitializeExperimenter(SubsessionMixIn, ptree.views.InitializeExperimenter):
    pass
