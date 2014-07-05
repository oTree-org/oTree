import lab_results.models as models

class ParticipantMixIn(object):
    z_models = models

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.treatment = models.Treatment()
        self.match = models.Match()
        self.participant = models.Participant()

class ExperimenterMixIn(object):

    z_models = models

    def z_autocomplete(self):
        self.subsession = models.Subsession()

import ptree.views
class InitializeParticipant(ParticipantMixIn, ptree.views.InitializeParticipant):
    pass
class InitializeExperimenter(ExperimenterMixIn, ptree.views.InitializeExperimenter):
    pass
