# Don't change anything in this file.
import battle_of_the_sexes.models as models
import ptree.views
import ptree.forms
import ptree.test
from ptree.common import Money, money_range

class Page(ptree.views.Page):
    z_models = models

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.treatment = models.Treatment()
        self.match = models.Match()
        self.participant = models.Participant()


class SubsessionWaitPage(ptree.views.SubsessionWaitPage):

    z_models = models

    def z_autocomplete(self):
        self.subsession = models.Subsession()


class MatchWaitPage(ptree.views.MatchWaitPage):

    z_models = models

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.treatment = models.Treatment()
        self.match = models.Match()

class Form(ptree.forms.Form):

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.treatment = models.Treatment()
        self.match = models.Match()
        self.participant = models.Participant()

class Bot(ptree.test.Bot):

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.treatment = models.Treatment()
        self.match = models.Match()
        self.participant = models.Participant()


class InitializeParticipant(ptree.views.InitializeParticipant):
    z_models = models


class InitializeExperimenter(ptree.views.InitializeExperimenter):
    z_models = models
