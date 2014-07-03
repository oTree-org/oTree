import lab_results.models as models

class ParticipantMixin(object):
    z_models = models

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.treatment = models.Treatment()
        self.match = models.Match()
        self.participant = models.Participant()

class ExperimenterMixin(object):

    z_models = models

    def z_autocomplete(self):
        self.subsession = models.Subsession()

import ptree.views
class InitializeParticipant(ParticipantMixin, ptree.views.InitializeParticipant):
    pass
class InitializeExperimenter(ExperimenterMixin, ptree.views.InitializeExperimenter):
    pass
