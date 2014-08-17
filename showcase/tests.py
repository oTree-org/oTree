import otree.test
import showcase.views as views
from showcase.utilities import Bot


class PlayerBot(Bot):

    def play(self):

        self.submit(views.Introduction)

        self.submit(views.FormsDemo, {
            'demo_field1': 'yes',
            'demo_field2': 'demo text',
            'demo_field3': 'sample text',
            'demo_field4': 'accept',
            'demo_field5': 3,
        })

        self.submit(views.EmbedDemo)

        self.submit(views.BootstrapWidgetDemo)

        #self.submit(views.AdminDemo)

        self.submit(views.Results)