# Don't change anything in this file.
import matrix_asymmetric.models as models
import ptree.views
import ptree.forms

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

class InitializeParticipant(ParticipantMixin, ptree.views.InitializeParticipant):
    pass

class InitializeExperimenter(ExperimenterMixin, ptree.views.InitializeExperimenter):
    pass
