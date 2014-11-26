# Don't change anything in this file.
import ultimatum.models as models
import otree.views


class PlayerMixin(object):
    z_models = models

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.treatment = models.Treatment()
        self.match = models.Match()
        self.particlayerdels.ParticipantlayerExperimenterMixin(object):

    z_models = models

    def z_autocomplete(self):
        self.subsession = models.Subsession()


class InitializeParticipant(Partlayerin, otrlayernitializeParticipant):
    pass

class InitializeExperimenter(ExperimenterMixin, otree.views.InitializeExperimenter):
    pass
