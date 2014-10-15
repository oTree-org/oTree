# This file is auto-generated. Don't change anything in this file.
import rock_paper_scissors.models as models
import otree.views
import otree.forms
import otree.test

class Page(otree.views.Page):
    z_models = models

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.group = models.Group()
        self.player = models.Player()


class WaitPage(otree.views.WaitPage):

    z_models = models

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.group = models.Group()

class Form(otree.forms.Form):

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.group = models.Group()
        self.player = models.Player()

class Bot(otree.test.Bot):

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.group = models.Group()
        self.player = models.Player()


class InitializePlayer(otree.views.InitializePlayer):
    z_models = models


class InitializeExperimenter(otree.views.InitializeExperimenter):
    z_models = models
