from survey._builtin import Bot
from survey import views


class PlayerBot(Bot):

    def play(self):

        self.submit(views.Demographics, {
            'q_country': 'BS',
            'q_age': 24,
            'q_gender': 'Male'})

        self.submit(views.CognitiveReflectionTest, {
            'crt_bat_float': 0.10,
            'crt_widget': 5,
            'crt_lake': 48
        })

        self.submit(views.End)
