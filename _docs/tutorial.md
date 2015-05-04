# oTree tutorial

Here are the steps to create a simple public goods game.

## Install oTree

Follow the instructions at [http://www.otree.org/download/](http://www.otree.org/download/)

## Create the app

Create the public goods app with this command:

`./otree startapp public_goods_simple`

Then go to the folder `public_goods_simple` that was created.

## Define models.py

Let's define our data model in `models.py`.

First, let's define our constants and parameters -- things that are the same for all players in all games:

* There are 3 players per group. So, let's change `players_per_group` to 3. Once this is done, oTree will automatically divide players into groups of 3.
* The endowment to each player is 100 points. So, let's define `endowment` and set it to `c(100)`. (`c()` means it is a currency amount; see the docs for more info).
* Each contribution is multiplied by 1.8. So let's define `efficiency_factor` and set it to 1.8:

Now we have:

```Python

class Constants:
    name_in_url = 'public_goods'
    players_per_group = 3
    num_rounds = 1

    endowment = c(100)
    efficiency_factor = 1.8
```

Now let's think about the entities in this game: the Player and the Group.

What data points are we interested in recording about each player? The main thing is how much they contributed.
So, we define a field `contribution`:

class Player(otree.models.BasePlayer):

    # ...

    contribution = models.CurrencyField(min=0, max=Constants.endowment)

```

What data points are we interested in recording about each group?
We might be interested in knowing the total contributions to the group,
and the individual share returned to each player.


```Python
class Group(otree.models.BaseGroup):

    # ...

    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
```

We also need to define the logic for how these fields get calculated. Let's define a method on the group called `set_payoffs`:

```Python
class Group(otree.models.BaseGroup):

    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            p.payoff = Constants.endowment - p.contribution + self.individual_share

```

## Define the template

Let's first create our HTML templates. This game will have 2 pages.

* Page 1: players decide how much to contribute
* Page 2: players are told the results

So, let's make 2 HTML files under `templates/public_goods_simple/`.

The first is `Contribute.html`.

```HTML+Django

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

The second template will be called `Results.html`.

```HTML+Django

{% extends "global/Base.html" %}
{% load staticfiles otree_tags %}

{% block title %}
    Results
{% endblock %}

{% block content %}

    <p>
        Your group contributed {{ group.total_contributions }},
        resulting in an individual share of {{ group.individual_share }}.
        Your profit is therefore:
    </p>

    <p>
    {{ Constants.endowment }} - {{ player.contribution }} + {{ group.individual_share }} = {{ player.payoff }}
    </p>


{% endblock %}

```

## Define views.py

Now we define our views, which decide the logic for how to display the HTML templates.

Since we have 2 templates, we need 2 view classes, with the same names as the templates (`Contribute` and `Results`).

First let's define `Contribute`. We need to define `form_model` and `form_fields` to specify that this page contains a form
letting you set `Player.contribution`:

```Python

class Contribute(Page):

    form_model = models.Player
    form_fields = ['contribution']

```

Now we define `Results`. This page doesn't have a form so our class definition can be empty (with the `pass` keyword).

```
class Results(Page):
    pass
```

We are almost done, but one more page is needed. After a player makes a contribution, they cannot see the results page
right away; they first need to wait for the other players to contribute. You therefore need to add a `WaitPage`.

When all players have completed the `Contribute` page, the players' payoffs can be calculated.
You can trigger this calculation inside the the `after_all_players_arrive` method on the `WaitPage`,
which automatically gets called when all players have arrived at the wait page:

```
class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()
```

Now we define `page_sequence` to specify the order in which the pages are shown:

```Python

page_sequence = [
    Contribute,
    ResultsWaitPage,
    Results
]

```

## Define the session type in settings.py

Now we go to `settings.py` and define a session type.
In many experiments, the user should fill out an 'exit survey'. You can add an exit survey by adding the app to
`app_sequence`.


```Python
SESSION_TYPES = [
    {
        'name': 'public_goods_simple',
        'display_name': "Public Goods (Simple Version)",
        'num_demo_participants': 3,
        'app_sequence': ['public_goods_simple', 'survey'],
    },
    # ...
```

## Reset the database and run

Before you run the server, you need to reset the database.
In the launcher, click the button "clear the database". Or, on the command line, run `./otree resetdb`.

Every time you add, change, or remove a field in `models.py`
This is because we have defined new fields in `models.py`,
and the SQL database needs to be re-generated to create these tables and columns.

Then, run the server and open your browser to [http://127.0.0.1:8000](http://127.0.0.1:8000) to play the game.