# Don't change anything in this file.
import guessing.models as models
import ptree.views
import ptree.forms

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
class InitializeParticipant(ParticipantMixIn, ptree.views.InitializeParticipant):
    pass

class InitializeExperimenter(SubsessionMixIn, ptree.views.InitializeExperimenter):
    pass
