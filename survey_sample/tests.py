from survey_sample._builtin import Bot
from survey_sample import views

class PlayerBot(Bot):

    def play(self):
        self.submit(views.Survey, {'q_gender': 'Male'})

