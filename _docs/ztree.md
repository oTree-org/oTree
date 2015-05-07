# Comparison with z-Tree

For those familiar with z-Tree, here are some examples of how some z-Tree
concepts are expressed in oTree. If you would like to request
an item added to this list,
please email chris@otree.org.

### z-Tree & z-Leafs

oTree is web-based so it does not have an equivalent of z-Leafs. As long as the oTree server
is running, you can open links on

### Treatments

In oTree, these are apps in `app_sequence` in `settings.py`.

### Periods

In oTree, these are called "rounds". You can set `num_rounds`, and get the current round number with
self.subsession.round_number.

### Stages

oTree calls these "pages", and they are defined in `views.py`.

### Subjects

oTree calls these 'players'

### Variables

In z-Tree you define variables that go in the subjects table.

In oTree, you define the structure of your table by defining "fields" in `models.py`.
Each field defines a column in the table, and has an associated data type (number, text, etc).

### Accessing data from previous periods and treatments

See the reference on `in_previous_rounds` and `participant.vars`.

### Participate

Each oTree page has an `is_displayed` method that returns True or False.

### Timeout

In oTree, define a `timeout_seconds` on your `Page`.
You can also optionally define `auto_submit_values`.

#

z-Tree:

`sum( same( Group ), Contribution );`

oTree:

`sum([p.contribution for p in self.group.get_players()])`

### Questionnaires

In oTree, questionnaires are not distinct from any other type of app.
You program them the same way as a normal oTree app. See the "survey" app for an example.

### Program evaluation

In z-Tree, programs are executed for each row in the current table, at the same time.

In oTree, code is executed individually as each participant progresses through the game.



For example, suppose you have this `Page`:

```Python

 class MyPage(Page):

    def vars_for_template(self):
        return {'double_contribution':

    def before_next_page(self):
        self.player.foo = True

```

The code in `vars_for_template` and `before_next_page`
is executed independently for a given participant when that participant enters and exits the page,
respectively.

If you want code to be executed for all participants at the same time,
it should go in `before_session_starts` or `after_all_players_arrive`.

## Tables

### Table functions

#### find()

Use `group.get_players()` to get all players in the same group, and `subsession.get_players()`
 to get all players in the same subsession.

If you want to filter the list of players for all that meet a certain condition,
e.g. all players in the subsession whose `payoff` is zero,
you would do:

```Python
zero_payoff_players = [p for p in self.subsession.get_players() if p.payoff == 0]
```

Another way of writing this is:

```Python
zero_payoff_players = []
for p in self.subsession.get_players():
 if p.payoff == 0:
    zero_payoff_players.append(p)
```

You can also use `group.get_player_by_id()` and `group.get_player_by_role()`.

Whereas the z-Tree language is table-oriented, Python is object-oriented.

oTree is based on Python.


#### Subjects table

You define variables for each player

the structure of your table

You can access all players like this:

`self.subsession.get_players()`

This returns a list of all players


#### Globals table

`self.session.vars` can hold global variables


### Groups

Set `players_per_group` to any number you desire.
When you create your session, you will be prompted to choose a number of participants.
oTree will then automatically divide these players into groups.

#### Player types

In z-Tree you set variables like:

```
PROPOSERTYPE = 1;
RESPONDERTYPE = 2;
```
And then depending on the subject you assign something like:

```
Type = PROPOSERTYPE
```

In oTree you can determine the player's type based on the automatically assigned field
`player.id_in_group`,
which is unique within the group (ranges from 1...N in an N-player group).

Additionally, you can define the method `role()` on the player:

```
def role(self):
    if self.id_in_group == 1:
        return 'proposer'
    else:
        return 'responder'
```

### Waiting screens

In oTree, participants can move through pages and subsessions individually.
Participants can be in different apps or rounds (i.e. treatments or periods) at the same time.

If you would like to restrict this independent movement, you can use oTree's equivalent of "Wait for all...",
which is to insert a `WaitPage` at the desired place in the `page_sequence`.

### History box

You can program a history box to your liking using `in_all_rounds`. For example:

```
    <table class="table">
        <tr>
            <th>Round</th>
            <th>Player and outcome</th>
            <th>Points</th>
        </tr>
        {% for p in player.in_all_rounds %}
            <tr>
                <td>{{ p.subsession.round_number }}</td>
                <td>You were {{ p.role }} and {% if p.is_winner %} won {% else %} lost {% endif %}</td>
                <td>{{ p.payoff }}</td>
            </tr>
        {% endfor %}
    </table>
```

### Parameters table

Define a method in `before_session_starts` that loops through all players in the subsession
and sets values for the fields.

## Money and currency

### Profit and TotalProfit

ShowUpFee: session_type.participation_fee
Profit: player.payoff
FinalProfit: participant.payoff
MoneyToPay: participant.money_to_pay()

### The equivalent of

### Experimental currency units (ECU)

The oTree equivalent of ECU is points, and the exchange rate is defined by `money_per_point`.

In oTree you also have the option to not use ECU and to instead play the game in real money.

## Layout

### Data display and input

In the HTML template, you output the current player's contribution like this:

```
 {{ player.contribution }}
```

If you need the player to input their contribution, you do it like this:

```
{% formfield player.contribution %}
```

### Layout: !text

In z-Tree you would do this:

```
<>Your income is < Profit | !text: 0="small"; 80 = "large";>.
```

In oTree you can use `vars_for_template`, for example:

```
def vars_for_template(self):
    if self.player.payoff > 40:
        size = 'large'
    else:
        size = 'small'
    return {'size': size}
```

Then in the template do:

```
Your income is {{ size }}.
```

Another way to accomplish this is the `get_FOO_display`, which is
described in the reference with the example about `get_year_in_school_display`.

## Code examples

z-Tree:
```
OthersChoice = find( same( Group ) & not( same( Subject ) ), Choice );
```

oTree:

```
others_choice = self.get_others_in_group()[0].choice
```

