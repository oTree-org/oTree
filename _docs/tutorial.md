# oTree tutorial

This tutorial will cover the creation of 2 games: a simple public goods game, and a simple trust game.
Before proceeding through this tutorial, install oTree according to the instructions at
[http://www.otree.org/download/](http://www.otree.org/download/)

# Part 1: Public goods game

We will now create a simple public goods game.
The completed app is [here](https://github.com/oTree-org/oTree/tree/master/public_goods_simple).

## Create the app

Create the public goods app with this command:

`./otree startapp public_goods_simple`

Then go to the folder `public_goods_simple` that was created.


## Define models.py

Let's define our data model in `models.py`.

First, let's modify the `Constants` class to define our constants and parameters -- things that are the same for all players in all games.

* There are 3 players per group. So, let's change `players_per_group` to 3. oTree will then automatically divide players into groups of 3.
* The endowment to each player is 100 points. So, let's define `endowment` and set it to `c(100)`. (`c()` means it is a currency amount; see the docs for more info).
* Each contribution is multiplied by 1.8. So let's define `efficiency_factor` and set it to 1.8:

Now we have:

```Python

class Constants:
    name_in_url = 'public_goods_simple'
    players_per_group = 3
    num_rounds = 1

    endowment = c(100)
    efficiency_factor = 1.8
```

Now let's think about the main entities in this game: the Player and the Group.

What data points are we interested in recording about each player? The main thing is how much they contributed.
So, we define a field `contribution`:

```Python
class Player(otree.models.BasePlayer):

    # ...

    contribution = models.CurrencyField(min=0, max=Constants.endowment)

```

What data points are we interested in recording about each group?
We might be interested in knowing the total contributions to the group,
and the individual share returned to each player.
So, we define those 2 fields:


```Python
class Group(otree.models.BaseGroup):

    # ...

    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
```

We also need to define the logic for how these fields get calculated. Let's define a method on the group called `set_payoffs`:

```Python
class Group(otree.models.BaseGroup):

    # ...

    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            p.payoff = Constants.endowment - p.contribution + self.individual_share

```

## Define the template

This game will have 2 pages.

* Page 1: players decide how much to contribute
* Page 2: players are told the results

So, let's make 2 HTML files under `templates/public_goods_simple/`.

The first is `Contribute.html`, which contains a brief explanation of the game,
and a form field where the player can enter their contribution.

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
        You started with an endowment of {{ Constants.endowment }}, of which you contributed {{ player.contribution }}.
        Your group contributed {{ group.total_contributions }},
        resulting in an individual share of {{ group.individual_share }}.
        Your profit is therefore {{ player.payoff }}:
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

There should be some logic in this wait page. When all players have completed the `Contribute` page,
the players' payoffs can be calculated.
You can trigger this calculation inside the the `after_all_players_arrive` method on the `WaitPage`,
which automatically gets called when all players have arrived at the wait page.
Another advantage of putting the code here is that it only gets executed once,
rather than being executed separately for each participant, which is redundant.

We write `self.group.set_payoffs()` because earlier we decided to name the payoff calculation method `set_payoffs`,
 and it's a method under the `Group` class. That's why we prefix it with `self.group`.

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

Now we go to `settings.py` and add an entry to `SESSION_TYPES`.
In lab experiments, it's typical for users to fill out an exit survey, and then see how much money they made.
So let's do this by adding the existing "exit survey" and "payment info" apps to
`app_sequence`.


```Python
SESSION_TYPES = [
    {
        'name': 'public_goods_simple',
        'display_name': "Public Goods (Simple Version)",
        'num_demo_participants': 3,
        'app_sequence': ['public_goods_simple', 'survey', 'payment_info'],
    },
    # ...
```

However, we must also remember to add a `{% next_button %}` element to the `Results.html`, so the user can click a button
taking them to the next app in the sequence.

## Reset the database and run

Before you run the server, you need to reset the database.
In the launcher, click the button "clear the database". Or, on the command line, run `./otree resetdb`.

Every time you add, change, or remove a field in `models.py`
This is because we have defined new fields in `models.py`,
and the SQL database needs to be re-generated to create these tables and columns.

Then, run the server and open your browser to [http://127.0.0.1:8000](http://127.0.0.1:8000) to play the game.

# Part 2: Trust game

Now let's create a Trust game, which is a different type of game, to allow us to highlight some different features of oTree.

This is a trust game with 2 players.

To start, Player 1 receives 10 points;
Player 2 receives nothing.
Player 1 can send some or all of his points to Player 2.
Before B receives these points they will be tripled.
Once B receives the tripled points he can decide to send some or all of his points to A.

The completed app is [here](https://github.com/oTree-org/oTree/tree/master/trust_simple).

## Create the app

`./otree startapp trust_simple`

## Define models.py

First we define our app's constants. The endowment is 10 points and the donation gets tripled.

```
class Constants:
    name_in_url = 'trust_simple'
    players_per_group = 2
    num_rounds = 1

    endowment = c(10)
    multiplication_factor = 3
```

Then we think about how to define fields on the data model.
There are 2 critical data points to capture: the "sent" amount from P1, and the "sent back" amount from P2.

Your first instinct may be to define the fields on the Player like this:

```
class Player(otree.models.BasePlayer):

    # <built-in>
    ...
    # </built-in>

    sent_amount = models.CurrencyField()
    sent_back_amount = models.CurrencyField()
```

The problem with this model is that `sent_amount` only applies to P1,
   and `sent_back_amount` only applies to P2.
   It does not make sense that P1 should have a field called `sent_back_amount`.
   How can we make our data model more accurate?

We can do it by defining those fields at the `Group` level.
This makes sense because each group has exactly 1 `sent_amount` and exactly 1 `sent_back_amount`:

```
class Group(otree.models.BaseGroup):

    # <built-in>
    ...
    # </built-in>

    sent_amount = models.CurrencyField()
    sent_back_amount = models.CurrencyField()
```

Even though it may not seem that important at this point,
modeling our data correctly will make the rest of our work easier.

Now we add more details: Let's let P1 choose from a dropdown menu how much to donate,
rather than entering free text. To do this, we use the `choices=` argument, as well as
the `currency_range` function:

```
    sent_amount = models.CurrencyField(
        choices=currency_range(0, Constants.endowment, c(1)),
    )
```

We'd also like P2 to use a dropdown menu to choose how much to send back,
but we can't specify a fixed list of `choices`, because P2's available choices depend on how much P1 donated.
I'll show a bit later how we can make this list dynamic.

Also, let's define the payoff function on the group:

```
    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = Constants.endowment - self.sent_amount + self.sent_back_amount
        p2.payoff = self.sent_amount * Constants.multiplication_factor - self.sent_back_amount
```


## Define the templates and views

We need 3 pages:

* P1's "Send" page
* P2's "Send back" page
* "Results" page that both users see.

It would also be good if game instructions appeared on each page so that players are clear how the game works.
We can define a file `Instructions.html` that gets included on each page.

### Instructions.html

This template uses Django's template inheritance with the `{% extends %}` command.
For basic apps you don't need to know the details of how template inheritance works.

```
{% extends "global/Instructions.html" %}

{% block instructions %}
<p>
    This is a trust game with 2 players.
</p>
<p>
    To start, participant A receives {{ Constants.endowment }};
    participant B receives nothing.
    Participant A can send some or all of his {{ Constants.endowment }} to participant B.
    Before B receives these points they will be tripled.
    Once B receives the tripled points he can decide to send some or all of his points to A.
</p>
{% endblock %}
```

### Send

This page looks like the templates we have seen so far.
Note the use of `{% include %}` to automatically insert another template.

```
{% extends "global/Base.html" %}
{% load staticfiles otree_tags %}

{% block title %}
    Trust Game: Your Choice
{% endblock %}

{% block content %}

    {% include 'trust_simple/Instructions.html' %}

    <p>
    You are Participant A. Now you have {{Constants.endowment}}.
    </p>

    {% formfield group.sent_amount with label="How much do you want to send to participant B?" %}

    {% next_button %}

{% endblock %}
```

We also define the view in views.py:

```
class Send(Page):

    form_model = models.Group
    form_fields = ['sent_amount']

    def is_displayed(self):
        return self.player.id_in_group == 1
```

The `{% formfield %}` in the template must match the `form_model` and `form_fields` in the view.

Also, we use `is_displayed` to only show this to P1; P2 skips the page.

### SendBack

This is the page that P2 sees to send money back. Here is the template:

```
{% extends "global/Base.html" %}
{% load staticfiles otree_tags %}

{% block title %}
    Trust Game: Your Choice
{% endblock %}

{% block content %}

    {% include 'trust_simple/Instructions.html' %}

<p>
You are Participant B. Participant A sent you {{group.sent_amount}} and you received {{tripled_amount}}.
</p>

    {% formfield group.sent_back_amount with label="How much do you want to send back?" %}

    {% next_button %}

{% endblock %}
```

Here is the code from views.py. Notes:

* We use `vars_for_template` to pass the variable `tripled_amount` to the template.
Django does not let you multiply numbers directly in a template,
so this number needs to be calculated in Python code and passed to the template.
* We define a method `sent_back_amount_choices` to populate the dropdown menu dynamically.
This is the feature called `{field_name}_choices`, which is explained in the reference documentation.

```
class SendBack(Page):

    form_model = models.Group
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        return {
            'tripled_amount': self.group.sent_amount * Constants.multiplication_factor
        }

    def sent_back_amount_choices(self):
        return currency_range(
            c(0),
            self.group.sent_amount * Constants.multiplication_factor,
            c(1) * Constants.multiplication_factor
        )
```

### Results

The results page needs to look slightly different for P1 vs. P2.
So, we use the `{% if %}` statement (part of [Django's template language](https://docs.djangoproject.com/en/1.7/topics/templates/))
to condition on the current player's `id_in_group`.

```
{% extends "global/Base.html" %}
{% load staticfiles otree_tags %}

{% block title %}
    Results
{% endblock %}

{% block content %}

{% if player.id_in_group == 1 %}
    <p>
        You sent Participant B {{ group.sent_amount }}.
        Participant B returned {{group.sent_back_amount}}.
    </p>
    {% else %}
    <p>
        Participant A sent you {{ group.sent_amount }}.
        You returned {{group.sent_back_amount}}.
    </p>

{% endif %}

    <p>
    Therefore, your total payoff is {{player.payoff}}.
    </p>

    {% include 'trust_simple/Instructions.html' %}

{% endblock %}

```

Here is the Python code for this page in views.py:

```
class Results(Page):

    def vars_for_template(self):
        return {
            'tripled_amount': self.group.sent_amount * Constants.multiplication_factor
        }
```

### Wait pages and page sequence

This game has 2 wait pages:

* P2 needs to wait while P1 decides how much to send
* P1 needs to wait while P2 decides how much to send back

After the second wait page, we should calculate the payoffs. So, we use `after_all_players_arrive`.

So, we define these pages:

```
class WaitForP1(WaitPage):
    pass

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

```

## Add an entry to `SESSION_TYPES` in `settings.py`

```
    {
        'name': 'trust_simple',
        'display_name': "Trust Game (simple version from tutorial)",
        'num_demo_participants': 2,
        'app_sequence': ['trust_simple'],
    },
```

## Reset the database and run

If you are on the command line, enter:

```
./otree resetdb
./otree runserver
```

If you are using the launcher, click the button equivalents to these commands.

Then open your browser to [http://127.0.0.1:8000](http://127.0.0.1:8000) to play the game.