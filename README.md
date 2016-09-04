# oTree

oTree is a Python framework for multiplayer strategy games, especially for economics and
psychology research. You can build games like the prisoner's dilemma, public goods games,
auctions, and surveys.

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

## Example game: public goods

Below is a full implementation of a [public goods game](https://en.wikipedia.org/wiki/Public_goods_game),
which you can play [here](http://otree-demo.herokuapp.com/demo/public_goods_simple/).

### models.py

```python
from otree.api import (
    BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models, Currency
)

class Constants(BaseConstants):
    name_in_url = 'public_goods_simple'
    players_per_group = 3
    num_rounds = 1
    endowment = Currency(100)
    efficiency_factor = 2

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()

    def set_payoffs(self):
        self.total_contribution = sum(p.contribution for p in self.get_players())
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            p.payoff = Constants.endowment - p.contribution + self.individual_share

class Player(BasePlayer):
    contribution = models.CurrencyField(min=0, max=Constants.endowment)
```

### views.py

```python
from otree.api import Page, WaitPage
from . import models

class Contribute(Page):
    form_model = models.Player
    form_fields = ['contribution']

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()

class Results(Page):
    pass

page_sequence = [Contribute, ResultsWaitPage, Results]
```

### Contribute.html

```django
{% extends "global/Base.html" %}
{% load staticfiles otree_tags %}

{% block title %}
    Contribute
{% endblock %}

{% block content %}

    <p>
        This is a public goods game with
        {{ Constants.players_per_group }} players per group,
        an endowment of {{ Constants.endowment }},
        and an efficiency factor of {{ Constants.efficiency_factor }}.
    </p>

    {% formfield player.contribution with label="How much will you contribute?" %}

    {% next_button %}

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

    <p>
        You started with an endowment of {{ Constants.endowment }},
        of which you contributed {{ player.contribution }}.
        Your group contributed {{ group.total_contribution }},
        resulting in an individual share of {{ group.individual_share }}.
        Your profit is therefore {{ player.payoff }}.
    </p>

    {% next_button %}

{% endblock %}
```

### bots.py (optional, for automated testing)

```python
from otree.api import Bot
from . import views

class PlayerBot(Bot):
    def play_round(self):
        yield (views.Contribute, {'contribution': 99})
        yield (views.Results)
```

## Features at a glance

- Publish your games to **Amazon Mechanical Turk**
- Program **bots** to simulate human players, can be used for multi-agent simulation.
- Flexible API for **group re-matching**

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
