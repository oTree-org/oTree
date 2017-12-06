# oTree

oTree is a framework based on Python and Django that lets you build:

- Multiplayer strategy games, like the prisoner's dilemma, public goods game, and auctions
- Controlled behavioral experiments in economics, psychology, and related fields
- Surveys and quizzes

## Live demo
http://demo.otree.org/

## Homepage
http://www.otree.org/

## Docs

http://otree.readthedocs.org

## Quick start

Rather than cloning this repo directly,
run these commands:

```
pip3 install -U otree-core
otree startproject oTree
otree resetdb
otree runserver
```

## Example game: guess 2/3 of the average

Below is a full implementation of the
[Guess 2/3 of the average](https://en.wikipedia.org/wiki/Guess_2/3_of_the_average) game,
where everyone guesses a number, and the winner is the person closest to 2/3 of the average.
The game is repeated for 3 rounds.
You can play the below game [here](http://otree-demo.herokuapp.com/demo/guess_two_thirds/).

### models.py

```python
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency
)

class Constants(BaseConstants):
    players_per_group = 3
    num_rounds = 3
    name_in_url = 'guess_two_thirds'

    jackpot = Currency(100)
    guess_max = 100


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

        self.best_guess = min(guesses,
            key=lambda guess: abs(guess - self.two_thirds_avg))

        winners = [p for p in players if p.guess == self.best_guess]
        self.num_winners = len(winners)

        for p in winners:
            p.is_winner = True
            p.payoff = Constants.jackpot / self.num_winners

    def two_thirds_avg_history(self):
        return [g.two_thirds_avg for g in self.in_previous_rounds()]


class Player(BasePlayer):
    guess = models.IntegerField(min=0, max=Constants.guess_max)
    is_winner = models.BooleanField(initial=False)
```

### views.py

```python
from . import models
from otree.api import Page, WaitPage


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1


class Guess(Page):
    form_model = models.Player
    form_fields = ['guess']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def vars_for_template(self):
        sorted_guesses = sorted(p.guess for p in self.group.get_players())

        return {'sorted_guesses': sorted_guesses}


page_sequence = [Introduction,
                 Guess,
                 ResultsWaitPage,
                 Results]
```

### HTML templates

[Instructions.html](https://github.com/oTree-org/oTree/blob/master/guess_two_thirds/templates/guess_two_thirds/Instructions.html)
[Introduction.html](https://github.com/oTree-org/oTree/blob/master/guess_two_thirds/templates/guess_two_thirds/Introduction.html)
[Guess.html](https://github.com/oTree-org/oTree/blob/master/guess_two_thirds/templates/guess_two_thirds/Guess.html)
[Results.html](https://github.com/oTree-org/oTree/blob/master/guess_two_thirds/templates/guess_two_thirds/Results.html)

### tests.py (optional)

Test bots for multiplayer games run in parallel, 
and can run either from the command line,
or in the browser, which you can try [here](http://otree-demo.herokuapp.com/demo/matching_pennies_bots/).

```python

from otree.api import Bot, SubmissionMustFail
from . import views
from .models import Constants

class PlayerBot(Bot):
    cases = ['p1_wins', 'p1_and_p2_win']

    def play_round(self):
        if self.subsession.round_number == 1:
            yield (views.Introduction)

        if self.case == 'p1_wins':
            if self.player.id_in_group == 1:
                for invalid_guess in [-1, 101]:
                    yield SubmissionMustFail(views.Guess, {"guess": invalid_guess})
                yield (views.Guess, {"guess": 9})
                assert self.player.payoff == Constants.jackpot
                assert 'you win' in self.html
            else:
                yield (views.Guess, {"guess": 10})
                assert self.player.payoff == 0
                assert 'you did not win' in self.html
        else:
            if self.player.id_in_group in [1, 2]:
                yield (views.Guess, {"guess": 9})
                assert self.player.payoff == Constants.jackpot / 2
                assert 'you are one of the 2 winners' in self.html
            else:
                yield (views.Guess, {"guess": 10})
                assert self.player.payoff == 0
                assert 'you did not win' in self.html

        yield (views.Results)
```

See docs on [bots](http://otree.readthedocs.io/en/latest/bots.html).


## Features 

- Easy-to-use admin interface for launching games & surveys, managing participants, monitoring data, etc.
- Simple yet extensive API
- Publish your games to Amazon Mechanical Turk


## Contact & support

[Help & discussion mailing list](https://groups.google.com/forum/#!forum/otree)

Contact chris@otree.org with bug reports.

## Contributors

* Gregor Muellegger (http://gremu.net/, https://github.com/gregmuellegger)
* Juan B. Cabral (http://jbcabral.org/, https://github.com/leliel12)
* Bertrand Bordage (https://github.com/BertrandBordage)
* Alexander Schepanovski (https://github.com/Suor/)
* Alexander Sandukovskiy
* Som Datye
* Benson Njogu (https://github.com/benarito)


## Related repositories

The oTree core libraries are [here](https://github.com/oTree-org/otree-core).
