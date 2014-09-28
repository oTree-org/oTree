# This file is auto-generated. Don't change anything in this file.
import common_value_auction.models as models
import otree.views
import otree.forms
import otree.test

class Page(otree.views.Page):
    z_models = models

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.treatment = models.Treatment()
        self.match = models.Match()
        self.player = models.Player()


class WaitPage(otree.views.WaitPage):

    z_models = models

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.treatment = models.Treatment()
        self.match = models.Match()

class Form(otree.forms.Form):

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.treatment = models.Treatment()
        self.match = models.Match()
        self.player = models.Player()

class Bot(otree.test.Bot):

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.treatment = models.Treatment()
        self.match = models.Match()
        self.player = models.Player()


class InitializePlayer(otree.views.InitializePlayer):
    z_models = models


class InitializeExperimenter(otree.views.InitializeExperimenter):
    z_models = models
