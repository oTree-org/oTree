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
    best_guess = models.PositiveIntegerField()
    num_winners = models.PositiveIntegerField()

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
    guess = models.PositiveIntegerField(max=Constants.guess_max)
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

### Instructions.html

```django
{% load otree_tags staticfiles %}

<div class="instructions well well-lg">

    <h3 class="panel-sub-heading">
        Instructions
    </h3>

    <p>
        You are in a group of {{ Constants.players_per_group }} people.
        Each of you will be asked to choose a
        number between 0 and {{ Constants.guess_max }}.
        The winner will be the participant whose
        number is closest to 2/3 of the
        average of all chosen numbers.
    </p>

    <p>
        The winner will receive {{ Constants.jackpot }}.
        In case of a tie, the {{ Constants.jackpot }}
        will be equally divided among winners.
    </p>

    <p>This game will be played for {{ Constants.num_rounds }} rounds.</p>

</div>
```

### Introduction.html

```django
{% extends "global/Base.html" %}
{% load staticfiles otree_tags %}

{% block title %}
    Introduction
{% endblock %}

{% block content %}

    {% include 'guess_two_thirds/Instructions.html' %}

    {% next_button %}

{% endblock %}
```

### Contribute.html

```django
{% extends "global/Base.html" %}
{% load staticfiles otree_tags %}

{% block title %}
    Your Guess
{% endblock %}

{% block content %}

    {% if player.round_number > 1 %}
        <p>
            Here were the two-thirds-average values in previous rounds:
            {{ group.two_thirds_avg_history }}
        </p>
    {% endif %}

    {% formfield player.guess with label="Please pick a number from 0 to 100:" %}
    {% next_button %}

    {% include 'guess_two_thirds/Instructions.html' %}

{% endblock %}
```

### Results.html

```django
{% extends "global/Base.html" %}
{% load staticfiles otree_tags %}

{% block title %}
    Results
{% endblock %}

{% block content %}

    <p>Here were the numbers guessed:</p>

    <p>
        {{ sorted_guesses }}
    </p>

    <p>
        Two-thirds of the average of these numbers is {{ group.two_thirds_avg }};
        the closest guess was {{ group.best_guess }}.
    </p>

    <p>Your guess was {{ player.guess }}.</p>

    <p>
        {% if player.is_winner %}
            {% if group.num_winners > 1 %}
                Therefore, you are one of the {{ group.num_winners }} winners
                who tied for the best guess.
            {% else %}
                Therefore, you win!
            {% endif %}
        {% else %}
            Therefore, you did not win.
        {% endif %}
    Your payoff is {{ player.payoff }}.
    </p>

    {% next_button %}

    {% include 'guess_two_thirds/Instructions.html' %}

{% endblock %}
```

## Features at a glance

- Program [bots](http://otree.readthedocs.io/en/latest/bots.html) to simulate human players, can be used for multi-agent simulation.
- Flexible API for [group re-matching](http://otree.readthedocs.io/en/latest/groups.html#group-matching)
- Publish your games to [Amazon Mechanical Turk](http://otree.readthedocs.io/en/latest/mturk.html)


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


## Related repositories

The oTree core libraries are [here](https://github.com/oTree-org/otree-core).
