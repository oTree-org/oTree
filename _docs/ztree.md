# oTree glossary for z-Tree programmers

For those familiar with z-Tree, here are some notes on the equivalents of various z-Tree
concepts in oTree. This document just gives the names of the oTree feature;
for full explanations of each concept, see the
[reference documentation](https://github.com/oTree-org/oTree/blob/master/README.md).

This list will expand over time. If you would like to request
an item added to this list, or if you have a correction to make,
please email chris@otree.org.

### z-Tree & z-Leafs

oTree is web-based so it does not have an equivalent of z-Leafs.
You run oTree on your server and then visit the site in the browser
of the clients.

### Treatments

In oTree, these are apps in `app_sequence` in `settings.py`.

### Periods

In oTree, these are called "rounds".
You can set `num_rounds`, and get the current round number with
self.subsession.round_number.

### Stages

oTree calls these "pages", and they are defined in `views.py`.

### Waiting screens

In oTree, participants can move through pages and subsessions individually.
Participants can be in different apps or rounds (i.e. treatments or periods) at the same time.

If you would like to restrict this independent movement,
you can use oTree's equivalent of "Wait for all...",
which is to insert a `WaitPage` at the desired place in the `page_sequence`.

### Subjects

oTree calls these 'players' or 'participants'. See the reference docs for
the distinction between players and participants.

### Participate=1

Each oTree page has an `is_displayed` method that returns True or False.

### Timeout

In oTree, define a `timeout_seconds` on your `Page`.
You can also optionally define `auto_submit_values`.

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

### Background programs

The closest equivalent is `before_session_starts`.

### Tables

#### Subjects table

In z-Tree you define variables that go in the subjects table.

In oTree, you define the structure of your table by defining "fields" in `models.py`.
Each field defines a column in the table, and has an associated data type (number, text, etc).

You can access all players like this:

`self.subsession.get_players()`

This returns a list of all players in the subsession.
Each player has the same set of fields, so this structure is conceptually
similar to a table.

oTree also has a "Group" object (essentially a "groups" table), where you can store data
at the group level, if it is not specific to any one player but rather the same
for all players in the group, like the total contribution by the group
(e.g. `self.group.total_contribution`).

#### Globals table

`self.session.vars` can hold global variables.

#### Table functions

oTree does not have table functions. If you want to carry out calculations over the whole table,
you should do so explicitly.

For example, in z-Tree:

```
S = sum(C)
```

In oTree you would do:

```
S = sum([p for p in self.subsession.get_players()])
```

##### find()

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


### Groups

Set `players_per_group` to any number you desire.
When you create your session, you will be prompted to choose a number of participants.
oTree will then automatically divide these players into groups.

#### Calculations on the group

For example:

z-Tree:

`sum( same( Group ), Contribution );`

oTree:

`sum([p.contribution for p in self.group.get_players()])`


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

### Accessing data from previous periods and treatments

See the reference on `in_all_rounds`, `in_previous_rounds` and `participant.vars`.

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

Any parameters that are constant within an app should be defined in `Constants` in `models.py`.
Some parameters are defined in `settings.py`.

Define a method in `before_session_starts` that loops through all players in the subsession
and sets values for the fields.

### Clients table

In the admin interface, when you run a session you can click on "Monitor".
This is similar to the z-Tree Clients table.

There is a button "Advance slowest participant(s)",
which is similar to z-Tree's "Leave stage" command.


### Money and currency

* ShowUpFee: session_type['participation_fee']
* Profit: player.payoff
* FinalProfit: participant.payoff
* MoneyToPay: participant.money_to_pay()

#### Experimental currency units (ECU)

The oTree equivalent of ECU is points, and the exchange rate is defined by `money_per_point`.

In oTree you also have the option to not use ECU and to instead play the game in real money.

### Layout

#### Data display and input

In the HTML template, you output the current player's contribution like this:

```
 {{ player.contribution }}
```

If you need the player to input their contribution, you do it like this:

```
{% formfield player.contribution %}
```

#### Layout: !text

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

## Miscellaneous code examples

### Get the other player's choice in a 2-person game

z-Tree:
```
OthersChoice = find( same( Group ) & not( same( Subject ) ), Choice );
```

oTree:

```
others_choice = self.get_others_in_group()[0].choice
```

### Check if a list is sorted smallest to largest

z-Tree (source: z-Tree mailing list):

```
iterator(i, 10 ).sum( iterator(j, 10 ).count( :i<j & ::values[ :i ] > ::values[ j ] )) ==0 
```

oTree:

```
values==sorted(values) 
```

### Randomly shuffle a list

z-Tree (source: z-Tree mailing list):

```
iterator(i, size_array - 1).do {
    address = roundup( random() * (:size_array + 1 - i), 1);
    if (address != :size_array + 1 - i) {
    temp = :random_sequence[:size_array + 1 - i];
    :random_sequence[:size_array + 1 - i] = :random_sequence[address];
    :random_sequence[address] = temp;
    }
}
```

oTree:

```
random.shuffle(random_sequence)
```

### Choose 3 random periods for payment

z-Tree: see [here](https://files.nyu.edu/awb257/public/slides/RandomRoundPayoffsTreatmentOrder.pdf):

oTree:

```
if self.subsession.round_number == Constants.num_rounds:
    random_players = random.sample(self.in_all_rounds(), 3)
    self.payoff = sum([p.potential_payoff for p in random_players])
```