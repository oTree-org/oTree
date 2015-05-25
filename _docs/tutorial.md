# oTree tutorial

This tutorial will cover the creation of 3 games:

* Public goods game
* Trust game
* Matching pennies

Before proceeding through this tutorial, install oTree according to the instructions at
[http://www.otree.org/download/](http://www.otree.org/download/)

# Part 1: Public goods game

We will now create a simple public goods game.
The completed app is [here](https://github.com/oTree-org/oTree/tree/master/public_goods_simple).

## Create the app

Create the public goods app with this command:

`python otree startapp public_goods_simple`

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
        Your group contributed {{ group.total_contribution }},
        resulting in an individual share of {{ group.individual_share }}.
        Your profit is therefore {{ player.payoff }}.
    </p>

{% endblock %}

```

## Define views.py

Now we define our views, which decide the logic for how to display the HTML templates.

Since we have 2 templates, we need 2 `Page` classes in `views.py`.
The names should match those of the templates (`Contribute` and `Results`).

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
In the launcher, click the button "clear the database". Or, on the command line, run `python otree resetdb`.

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

`python otree startapp trust_simple`

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

Note that we write `self.player.id_in_group`, because this is in `views.py`.

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
Django does not let you do calculations directly in a template,
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
            c(1)
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

Then we define the page sequence:

```
page_sequence = [
    Send,
    WaitForP1,
    SendBack,
    ResultsWaitPage,
    Results,
]
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
python otree resetdb
python otree runserver
```

If you are using the launcher, click the button equivalents to these commands.

Then open your browser to [http://127.0.0.1:8000](http://127.0.0.1:8000) to play the game.

# Part 3: Matching pennies

We will now create a "Matching pennies" game with the following features:

* 4 rounds
* The roles of the players will be reversed halfway through
* In each round, a "history box" will display the results of previous rounds
* A random round will be chosen for payment

The completed app is [here](https://github.com/oTree-org/oTree/tree/master/matching_pennies_tutorial).

## Update otree-core

For this game to work, you need otree-core >= 0.3.3, which contains important bugfixes.

If you installed oTree prior to 2015-05-25, you need to update your `requirements_base.txt`
to the latest version [here](https://github.com/oTree-org/oTree/blob/master/requirements_base.txt)
and then do:

```
  pip install -r requirements_base.txt
```

## Create the app

`python otree startapp matching_pennies_tutorial`

## Define models.py

We define our constants as we have previously.
Matching pennies is a 2-person game,
and the payoff for winning a paying round is 100 points.

```
class Constants:
    name_in_url = 'matching_pennies_tutorial'
    players_per_group = 2
    num_rounds = 4
    stakes = c(100)
```

Now let's define our `Player` class:

* In each round, each player decides "Heads" or "Tails", so we define a field `penny_side`,
which will be displayed as a radio button.
* We also have a boolean field `is_winner` that records if this player won this round.
* We define the `role` method to define which player is the "Matcher" and which is the "Mismatcher".

So we have:

```
class Player(otree.models.BasePlayer):

    # <built-in>
    # ...
    # </built-in>

    penny_side = models.CharField(
        choices=['Heads', 'Tails'],
        widget=widgets.RadioSelect()
    )

    is_winner = models.BooleanField()

    def role(self):
        if self.id_in_group == 1:
            return 'Mismatcher'
        if self.id_in_group == 2:
            return 'Matcher'
```

Now let's define the code to randomly choose a round for payment.
Let's define the code in `Subsession.before_session_starts`,
which is the place to put global code that initializes the state of the game,
before gameplay starts.

The value of the chosen round is "global" rather than different for each participant,
so the logical place to store it is as a "global" variable in `self.session.vars`.

So, we start by writing something like this,
which chooses a random integer between 1 and 4,
 and then assigns it into `session.vars`:

```
class Subsession(otree.models.BaseSubsession):

    def before_session_starts(self):
        paying_round = random.randint(1, Constants.num_rounds)
        self.session.vars['paying_round'] = paying_round
```

There is a slight mistake, however.
Because there are 4 rounds (i.e. subsessions), this code will get executed 4 times,
each time overwriting the previous value of `session.vars['paying_round']`, which is superfluous.
We can fix this with an `if` statement that makes it only run once (on the first round):

```
class Subsession(otree.models.BaseSubsession):

    def before_session_starts(self):
        if self.round_number == 1:
            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round
```

Now, let's also define the code to swap roles halfway through.
This kind of group-shuffling code should also go in `before_session_starts`.
We put it after our existing code.

In oTree, groups are randomly determined in the first round,
and in each round, the groups are kept the same as the previous round,
 unless you shuffle them. So, at the beginning of round 3,
 we should do the shuffle.
 (So that the groups will be in opposite order during rounds 3 and 4.)

 We use `group.get_players()` to get the ordered list of players in each group,
 and then reverse it (e.g. the list `[P1, P2]` becomes `[P2, P1]`).
 Then we use `group.set_players()` to set this as the new group order:

```
class Subsession(otree.models.BaseSubsession):

    def before_session_starts(self):
        if self.round_number == 1:
            ...
        if self.round_number == 3:
            # reverse the roles
            for group in self.get_groups():
                players = group.get_players()
                players.reverse()
                group.set_players(players)
```

Now we define our `Group` class.
We define the payoff method. We use `get_player_by_role` to fetch each of the 2 players in the group.
We could also use `get_player_by_id`, but I find it easier to identify the players
 by their roles as matcher/mismatcher.
Then, depending on whether the penny sides match, we either make P1 or P2 the winner.

So, we start with this:

```
class Group(otree.models.BaseGroup):

    # <built-in>
    ...
    # </built-in>


    def set_payoffs(self):
        matcher = self.get_player_by_role('Matcher')
        mismatcher = self.get_player_by_role('Mismatcher')

        if matcher.penny_side == mismatcher.penny_side:
            matcher.is_winner = True
            mismatcher.is_winner = False
        else:
            matcher.is_winner = False
            mismatcher.is_winner = True
```

We should expand this code by setting the actual `payoff` field.
However, the player should only receive a payoff if the current round is the randomly chosen paying round.
Otherwise, the payoff should be 0 points.
So, we check the current round number and compare it against the value we previously stored in `session.vars`.
We loop through both players (`[P1,P2]`, or `[mismatcher, matcher]`) and do the same check for both of them.

```
class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


    def set_payoffs(self):
        matcher = self.get_player_by_role('Matcher')
        mismatcher = self.get_player_by_role('Mismatcher')

        if matcher.penny_side == mismatcher.penny_side:
            matcher.is_winner = True
            mismatcher.is_winner = False
        else:
            matcher.is_winner = False
            mismatcher.is_winner = True
        for player in [mismatcher, matcher]:
            if self.subsession.round_number == self.session.vars['paying_round'] and player.is_winner:
                player.payoff = Constants.stakes
            else:
                player.payoff = c(0)
```

## Define the templates and views

This game essentially 2 pages:
* A `Choice` page that gets repeated for each round. The user is asked to choose heads/tails,
and they are also shown a "history box" showing the results of previous rounds.
* A `ResultsSummary` page that only gets displayed once at the end,
and tells the user their final payoff.

### Choice

In `views.py`, we define the `Choice` page.
This page should contain a form field that sets `player.penny_side`,
so we set `form_model` and `form_fields`.

Also, on this page we would like to display a "history box" table
that shows the result of all previous rounds.
So, we can use `player.in_previous_rounds()`, which returns a list
referring to the same participant in rounds 1, 2, 3, etc.
(For more on the distinction between "player" and "participant", see the reference docs.)

```
class Choice(Page):

    form_model = models.Player
    form_fields = ['penny_side']

    def vars_for_template(self):
        return {
            'player_in_previous_rounds': self.player.in_previous_rounds(),
        }
```

We then create a template `Choice.html` below.
This is similar to the templates we have previously created,
but note the `{% for %}` loop that creates all rows in the history table.
`{% for %}` is part of the Django template language.

```
{% extends "global/Base.html" %}
{% load staticfiles otree_tags %}

{% block title %}
    Round {{ subsession.round_number }} of {{ Constants.num_rounds }}
{% endblock %}

{% block content %}

    <h4>Instructions</h4>
    <p>
        This is a matching pennies game.
        Player 1 is the 'Mismatcher' and wins if the choices mismatch;
        Player 2 is the 'Matcher' and wins if they match.

    </p>

    <p>
        At the end, a random round will be chosen for payment.
    </p>

    <h4>Round history</h4>
    <table class="table">
        <tr>
            <th>Round</th>
            <th>Player and outcome</th>
        </tr>
        {% for p in player_in_previous_rounds %}
            <tr>
                <td>{{ p.subsession.round_number }}</td>
                <td>You were the {{ p.role }} and {% if p.is_winner %} won {% else %} lost {% endif %}</td>
            </tr>
        {% endfor %}
    </table>

    <p>
        In this round, you are the {{ player.role }}.
    </p>

    {% formfield player.penny_side with label="I choose:" %}

    {% next_button %}

{% endblock %}
```

### ResultsWaitPage

Before a player proceeds to the next round`s `Choice` page,
 they need to wait for the other player to complete the `Choice` page as well.
 So, as usual, we use a `WaitPage`.
 Also, once both players have arrived at the wait page, we call the `set_payoffs` method we defined earlier.

```
class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()
```

### ResultsSummary

Let's create `ResultsSummary.html`:

```
{% extends "global/Base.html" %}
{% load staticfiles otree_tags %}

{% block title %}
    Final results
{% endblock %}

{% block content %}

    <table class="table">
        <tr>
            <th>Round</th>
            <th>Player and outcome</th>
        </tr>
        {% for p in player_in_all_rounds %}
            <tr>
                <td>{{ p.subsession.round_number }}</td>
                <td>You were the {{ p.role }} and {% if p.is_winner %} won {% else %} lost {% endif %}</td>
            </tr>
        {% endfor %}
    </table>

    <p>
        The paying round was {{ paying_round }}.
        Your total payoff is therefore {{ total_payoff }}.
    </p>


{% endblock %}
```

Now we define the corresponding class in views.py.

* It only gets shown in the last round, so we set `is_displayed` accordingly.
* We retrieve the value of `paying_round` from `session.vars`
* We get the user's total payoff by summing up how much they made in each round.
* We pass the round history to the template with `player.in_all_rounds()`

In the `Choice` page we used `in_previous_rounds`, but here we use `in_all_rounds`.
This is because we also want to include the result of the current round.


```
class ResultsSummary(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):

        return {
            'total_payoff': sum([p.payoff for p in self.player.in_all_rounds()]),
            'paying_round': self.session.vars['paying_round'],
            'player_in_all_rounds': self.player.in_all_rounds(),
        }
```

The payoff is calculated in a Python "list comprehension".
 These are frequently used in the oTree sample games,
 so if you are curious you can read online about how list comprehensions work.
 The same code could be written as:

```
total_payoff = 0
for p in self.player.in_all_rounds():
   total_payoff += p.payoff

return {
    'total_payoff': total_payoff,
    ...
```

### Page sequence

Now we define the `page_sequence`:

```
page_sequence = [
    Choice,
    ResultsWaitPage,
    ResultsSummary
]
```

This page sequence will loop for each round.
However, `ResultsSummary` is skipped in every round except the last, because of how we set `is_displayed`,
resulting in this sequence of pages:

* Choice [Round 1]
* ResultsWaitPage [Round 1]
* Choice [Round 2]
* ResultsWaitPage [Round 2]
* Choice [Round 3]
* ResultsWaitPage [Round 3]
* Choice [Round 4]
* ResultsWaitPage [Round 4]
* ResultsSummary [Round 4]

## Add an entry to `SESSION_TYPES` in `settings.py`

When we run a real experiment in the lab, we will want multiple groups,
but to test the demo we just set `num_demo_participants` to 2,
meaning there will be 1 group.

```
    {
        'name': 'matching_pennies_tutorial',
        'display_name': "Matching Pennies (tutorial version)",
        'num_demo_participants': 2,
        'app_sequence': [
            'matching_pennies_tutorial',
        ],
    },
```

## Reset the database and run

```
python otree resetdb
python otree runserver
```
