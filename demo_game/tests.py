import otree.test
import demo_game.views as views
from demo_game._builtin import Bot


class PlayerBot(Bot):

    def play(self):

        self.submit(views.Introduction)

        self.submit(views.QuestionOne, {
            'demo_field1': 'yes',
        })

        self.submit(views.FeedbackOne)

        self.submit(views.QuestionTwo, {
            'demo_field2': 'Embed images',
        })

        self.submit(views.FeedbackTwo)

        self.submit(views.FormsDemo)

        self.submit(views.Results)

        self.submit(views.Finish)