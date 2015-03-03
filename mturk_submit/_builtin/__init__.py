# This file is auto-generated. Don't change anything in this file.

import otree.views
import otree.test

from .. import models


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


class Bot(otree.test.Bot):

    def z_autocomplete(self):
        self.subsession = models.Subsession()
        self.group = models.Group()
        self.player = models.Player()


