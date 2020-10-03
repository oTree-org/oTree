from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency,
)


doc = """
a.k.a. Keynesian beauty contest.

Players all guess a number; whoever guesses closest to
2/3 of the average wins.

See https://en.wikipedia.org/wiki/Guess_2/3_of_the_average
"""


class Constants(BaseConstants):
    players_per_group = 3
    num_rounds = 3
    name_in_url = 'guess_two_thirds'

    jackpot = Currency(100)
    guess_max = 100

    instructions_template = 'guess_two_thirds/instructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    two_thirds_avg = models.FloatField()
    best_guess = models.IntegerField()
    num_winners = models.IntegerField()

    def set_payoffs(self):
        players = self.get_players()
        guesses = [p.guess for p in players]
        two_thirds_avg = (2 / 3) * sum(guesses) / len(players)
        self.two_thirds_avg = round(two_thirds_avg, 2)

        self.best_guess = min(
            guesses, key=lambda guess: abs(guess - self.two_thirds_avg)
        )

        winners = [p for p in players if p.guess == self.best_guess]
        self.num_winners = len(winners)

        for p in winners:
            p.is_winner = True
            p.payoff = Constants.jackpot / self.num_winners

    def two_thirds_avg_history(self):
        return [g.two_thirds_avg for g in self.in_previous_rounds()]


class Player(BasePlayer):
    guess = models.IntegerField(
        min=0, max=Constants.guess_max, label="Please pick a number from 0 to 100:"
    )
    is_winner = models.BooleanField(initial=False)
