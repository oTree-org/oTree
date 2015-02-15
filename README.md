## Live demo
http://demo.otree.org/

## Homepage
http://www.otree.org/

## About

oTree is a Django-based framework for implementing multiplayer decision strategy games. 
Many of the details of writing a web application are abstracted away, 
meaning that the code is focused on the logic of the game.
oTree programming is accessible to programmers without advanced experience in web app development.

See the live demo [here](http://demo.otree.org/).

This repository contains the games; the oTree core libraries are [here](https://github.com/oTree-org/otree-core).


## Contact
chris@otree.org (you can also add me on Skype by searching this email address; please mention oTree in your contact request)

Please contact me if you find any bugs or issues in oTree or this documentation. oTree is under heavy development, therefore documentation might contain discrepancies with actual API.

## Quick start

    pip install -r requirements_base.txt
    ./otree resetdb
    ./otree runserver

### Prerequisites

### Python interpreter

Install [Python 2.7](https://www.python.org/download/releases/2.7.7/).

On Windows, select the option to add Python to your PATH while installing.

On Mac/Unix, it is very likely that Python is already installed. Open the Terminal and write ``python`` and hit Enter. If you get something like `-bash: python: command not found` you will have to install it yourself.

### PyCharm

To ease the learning curve of oTree, we strongly recommend using [PyCharm Professional](http://www.jetbrains.com/pycharm/), even though there are many other good editors for Python code. This is because:

* PyCharm has features that make oTree/Django development easier
* oTree has special integration with PyCharm's code completion functionality
* This documentation gives instructions assuming you are using PyCharm
* oTree has been thoroughly tested with PyCharm

If you are a student, teacher, or professor, PyCharm Professional is [free](https://www.jetbrains.com/student/). Note: we recommend PyCharm Professional rather than PyCharm Community Edition.


_TODO:_
* runserver & debug


## Setup

### Installer

You can download the installer [here](http://www.otree.org/download/)


### Manual setup

An alternative to using the installer is to do a command-line manual setup.

Install Git:
* On Windows, install [msysgit](http://msysgit.github.io/) (during installation, select the option to add git to your path)
* [TODO: Mac]

#### Pip

You will need a program called Pip in order to install packages.

Then, download [get-pip.py](https://raw.github.com/pypa/pip/master/contrib/get-pip.py).

On Windows, right-click the Windows PowerShell app icon, then click "Run as administrator" and run this command:

`python get-pip.py`

On Mac/Unix, run:

`sudo python get-pip.py`

You will be asked to enter the admin password.


#### Clone the repository

1. Open Terminal (for Mac and Linux users) or the command line (for Windows users).
2. On GitHub, navigate to your folder on your computer where you want your oTree repository to reside.
3. Enter `git clone https://github.com/oTree-org/oTree.git`

#### Install dependencies
Change into the `oTree` directory (the one containing `requirements_base.txt`), and run the following command:

`pip install -r requirements_base.txt`

#### Create the database

Run the following command (which creates the database):

`./otree resetdb`
	
#### Test that it worked

Run the command `./otree runserver`.
You should see the following output on the command line::

    Validating models...

    0 errors found
    |today| - 15:50:53
    Django version |version|, using settings 'settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Now that the server's running, visit `http://127.0.0.1:8000/` with your Web
browser.

## Sessions

In oTree, the term "session" refers to an event where a group of people spend time taking part in oTree experiments.

An example of a session would be: 

> On Tuesday at 3PM, 30 people will come to the lab for 1 hour, during which time they will play a trust game, followed by 2 ultimatum games, followed by a questionnaire. Participants get paid EUR 10.00 for showing up, plus bonus amounts for participating.

A session can be broken down into what oTree calls "subsessions". These are interchangeable units or modules that come one after another. Each subsession has a sequence of one or more pages the player must interact with. The session in the above example had 4 subsessions:

* Trust game
* Ultimatum game 1
* Ultimatum game 2
* Questionnaire

Each subsession is created by an oTree app. The above session would require 3 distinct apps to be coded:

* Trust game
* Ultimatum game
* Questionnaire

You can define your session's properties in `settings.py`. Here are the parameters for the above example:

         {
        'name':'my_session',
        'fixed_pay':1000,
        'app_sequence':['trust', 'ultimatum', 'questionnaire'],
         }

## Players vs. participants

In oTree, the terms "player" and "participant" have distinct meanings.

A participant is a person who takes part in a session. The participant object contains properties such as the participant's name, how much they made in the session, and what their progress is in the session.

A player is an instance of a participant in one particular subsession. A participant can be player 1 in the first subsession, player 5 in the next subsession, and so on.

Each player has an attribute called participant that refers to the participant. In the above example, here is how this participant would be modeled in oTree:

* participant
    * label: "John Smith"
    * time_started: "3 PM"
    * players:
        * player in trust subsession
            * bonus: $0.50
        * player in ultimatum subsession 1
            * bonus: $0.65
        * player in ultimatum subsession 2
            * bonus: $0.80
        * player in questionnaire subsession
            * bonus: $0.00
    * total bonuses for participant: ($0.50 + $0.65 + $0.80 + $0.00) = $1.95

## Apps

This page describes how to write a oTree app.

## Creating the app

First, choose a name for your app that is descriptive and short,
since you will be typing it and using it frequently. See existing games in the library for examples.

At your command line, go inside your project directory (the directory containing the file `otree`),
and run this command, where `your_app_name` is the name you have chosen for your app:

    ./otree startapp your_app_name

This will create a new app based on a oTree template, with most of the structure already set up for you.

Think of this as a skeleton to which you can add as much as you want.
You can add your own classes, functions, methods, and attributes,
or import any 3rd-party modules.

## Open your project for editing


Launch PyCharm, and select "Open Directory".
Navigate to your oTree directory (the directory containing the file `otree`) and click OK.
When the project opens, on the left-hand site you should see a directory tree that expands to the following::

    otree_experiments/
        <your_app_name>
            static/
            templates/
            _builtin/
                __init__.py
                admin.py                
            __init__.py
            models.py
            tests.py
            views.py


Then go to `settings.py` and create an entry for your app in SESSION_TYPES that looks like the other entries.

## Models

The purpose of running an experiment is to record data:
* what treatments are in your expefriment, what games were played in those treatments,
* what the results were,
* what actions the players took, etc.

oTree stores your data in standard database tables (SQL), which you can later export to CSV for analysis in Stata, R, Matlab, Excel, etc.

For example, let's say you are programming an ultimatum game, where in each two-person group, one player makes a monetary offer (say, 0-100 cents), and another player either rejects or accepts the offer. When you analyze your data, you will want your "Group" table to look something like this:

    +----------+----------------+----------------+ 
    | Group ID | Amount offered | Offer accepted |
    +==========+================+================+
    | 1        | 50             | TRUE           |
    +----------+----------------+----------------+ 
    | 2        | 25             | FALSE          |
    +----------+----------------+----------------+ 
    | 3        | 50             | TRUE           |
    +----------+----------------+----------------+ 
    | 4        | 0              | FALSE          |
    +----------+----------------+----------------+ 
    | 5        | 60             | TRUE           |
    +----------+----------------+----------------+ 

In order to end up with this table schema, you need to define a Django model, which is a Python class that defines a database table. You define what fields (columns) are in the table, what their data types are, and so on. When you run your experiment, the SQL tables will get automatically generated, and each time users visit, new rows will get added to the tables.

Here is what the model might look like for the above "Group" table::

    class Group(otree.models.BaseGroup):
        ...
        amount_offered = models.CurrencyField()
        offer_accepted = models.BooleanField()
    
This class will be placed in your app's `models.py` file.

Every oTree app needs the following 3 models:

* Player
* Group
* Subsession

They are related to each other as follows:

A player is part of a group, which is part of a subsession.

### Technical details
Each model has pointers to the parent models. A player object has attributes called `group` and `subsession`; a group object has a `subsession`.

Each model also has pointers to its child models. A `subsession` has methods called `get_players()`, and `get_groups()`. For example, entering `.get_players()` on a subsession will return a list of player contained in that subsession. Likewise, a group has a `get_players()` method.

Each model field you define can also have a `doc=` argument. Any string you add here will be included in the autogenerated documentation file, which can be downloaded through the data export page in the admin.

### Constants
`Constants` is a place to put your app's parameters and other constants.

These constants are required:
* `players_per_group` should be set to the number of players in a group of this game type. For example, in a 2-player game like an ultimatum game or prisoner's dilemma, you would set this to 2. If your app does not involve dividing the players into multiple groups, then set it to `None`. e.g. it is a single-player game or an auction where everybody in the subsession interacts together as 1 group. In this case, `self.group.get_players()` will return everybody in the subsession.
* `num_rounds` is the number of rounds this game should be played
* `name_in_url` is an attribute that defines the name this app has in the URLs, which players may see.


### Player

A player represents a person who participates in the subsession. The player object will store the results of that player's actions.

#### Implementation

The `payoff` field stores the monetary payoff the player gets paid for the current subsession (meaning `self.payoff = 1.20` sets the payoff to $1.20 (or, depending on your currency code, €1.20, etc.). You should set the payoff at some point in the subsession, usually on a wait page before the results page, when the player has fully completed their task. A good practice is to have a method on the group called `set_payoffs()` and call this method in the last wait page.

The field `id_in_group` is an index starting from 1. This is useful in multiplayer games where players have different roles, so that you can determine if the player is player 1, player 2, or so on.

The methods `get_others_in_group()` and `get_others_in_subsession()` returns a list of the other players in the group and subsession, respectively.

### Group

Groups represent multiplayer games, where there is some interaction between players. Example of a group: "an ultimatum game between players Alice and Bob, where Alice gave offered to give $0.50".

On your group model you can define fields to store the results of a particular group (e.g. what the score was).

Groups have a method called `get_player_by_id()`. The argument to this method is an integer; this function retrieves the player in the group whose `id_in_group` is that integer. So to get player 1 in a group, you would do `p1 = self.group.get_player_by_id()`.

There is also a similar method `get_player_by_role()`. The argument to this method is a string that looks up the player by their role value. (If you use this method, you must define the `role` method on the player model, which should return a string that depends on `id_in_group`.)

### Subsession

Your subsession model can define any fields that are common to all players in the subsession.

### Validation

oTree automatically validates all input submitted by the user.
For example, if you have a form containing a `PositiveIntegerField`,
oTree will not let the user submit values that are not positive integers, like `-1`, `1.5`, or `hello`.

Additionally, you can define one of the below methods in your `Page` class in `views.py`.

#### `def {field_name}_bounds(self)`

If you want to constrain the allowable answers for a field to a numeric range, you can define this method,
which should return a list with 2 elements, specifying the lower and upper bounds,  e.g. `return [24, 48]`

#### `def {field_name}_choices(self)`

If this method is defined, the default form widget will be a select box with these choices instead of the standard text field. This should return a list of values. If you would like a specially formatted value displayed to the user, you can return a list consisting itself of tuples of exactly two items (e.g. [(A, B), (A, B) ...]) to use as choices for this field. The first element in each tuple is the actual value to be set on the model, and the second element is the human-readable name. For example:

    def year_in_school_choices(self):
        return [
            ('FR', 'Freshman'),
            ('SO', 'Sophomore'),
            ('JR', 'Junior'),
            ('SR', 'Senior'),
    ]


#### `def {field_name}_error_message(self, value)`


Additionally, You can define a method called `[your field name]_error_message` that does additional validation of any form field.

For example, let's say your form has a field called `amount_returned`, which cannot be greater than the group's `amount_offered`. You would enforce this as follows:

    def amount_returned_error_message(self, value):
        if value > self.group.amount_offered:
            return 'Amount returned cannot be greater than amount offered'
            
            
## Views

Each page that your players see is defined by a `Page` class in `views.py`. (You can think of "views" as a synonym for "pages".)

For example, if your experiment involves showing the player a sequence of 5 pages, your `views.py` should contain 5 page classes.

At the bottom of your `views.py`, you must have a `page_sequence` variable that specifies the order in which players are routed through your pages. For example:

     page_sequence=[
        Start, Offer, Accept, Results]

This function should list all pages that anybody will see. You can filter individual pages from being seen.

The player must submit a valid form before they get routed to the next page. If the form they submit is invalid (e.g. missing or incorrect values), it will be re-displayed to them along with the list of errors they need to correct.

Here is what the code of a page should define (along with what attribute/method defines it):

## Page

### `player, group, subsession`
These attributes are provided automatically. For example, inside a method definition, you can access the current player with `self.player`, just as you can in `models.py` or `forms.py`.

### `template_name`

The name of the HTML template to display.

Example:

    # This will look inside your app under the 'templates' directory, 
    # to '/app_name/MyView.html'
    template_name = 'app_name/MyView.html'
    
### `form_models`

The model that this form modifies. It will most commonly be `models.Player` or `models.Group`.

### `form_fields`

A list of the field names from the model specified in `form_model` to include in the form.

### `timeout_seconds`

Set to an integer that specifies how many seconds the user has to complete the page. After the time runs out, the page
  auto-submits.

Example: `timeout_seconds = 20`

### `auto_submit_values`

Lets you specify what values should be auto-submitted if `timeout_seconds` is exceeded, or if the experimenter
moves the participant forward. If this is omitted, then oTree will default to `0` for numeric fields, `False` for boolean
fields, and the empty string for text/character fields.

This should be a dictionary where the keys are the elements of `form_fields`, and the values are the values that should
be auto-submitted.


### `def vars_for_template(self)`

oTree automatically passes Group, Player and Subsession objects to the template, so you can access them in the following format: `{{Constants.payoff_if_rejected}}`

Get any variables that will be passed to the HTML template. Add them to the dictionary as key-value pairs.

Example:

    def vars_for_template(self):
        return {'max_amount_offered': self.subsession.max_amount_offered,
                'reject_payoff': Constants.payoff_if_rejected}

Note that this method will be re-executed each time the player refreshes the page reloads the page (or submits an invalid form, which triggers a page reload). Make sure this doesn't cause undesired behavior. For example, if your code generates a payoff for the player based on a random number generator, the player could exploit this by refreshing the page until they get the payoff they want. To prevent issues like this, you can check if this variable has already been set, like this:

    if self.player.payoff is None:
        self.player.payoff = randint(0,100)

### `def is_displayed(self)`

Should return True if the page should be shown, and False if the page should be skipped. Default behavior is to show the page.

For example, if you only want a page to be shown to P2 in each group:

    def is_displayed(self):
        return self.player.id_in_group == 2
    
### `def after_next_button(self)`

After the player clicks the "Next" button, oTree makes sure that any form fields validate (and re-displays to the player with errors otherwise).

Here you can put anything additional that should happen after form validation. If you don't need anything to be done, it's OK to leave this method blank, or to leave it out entirely.

## `def vars_for_all_templates(self)`

This function is useful when you need certain variables to be passed to multiple pages in your app.
Instead of repeating the same values in each `vars_for_template`, you can define it in this function at the top of your views.py.

## Wait pages

Wait pages are created by subclassing from `WaitPage`.

If you have a wait page in your sequence of pages, then oTree waits until all players in the group have arrived at that point in the sequence, and then all players are allowed to proceed.

If your subsession has multiple groups playing simultaneously, and you would like a wait page that waits for all groups (i.e. all players in the subsession), you can set the attribute `wait_for_all_groups = True` on the wait page.

Wait pages can define the following methods:

### `def after_all_players_arrive(self)`

This code will be executed once all players have arrived at the wait page. For example, this method can determine the winner of an auction and set each player's payoff.

### `def title_text(self)`

The text in the title of the wait page.

### `def body_text(self)`

The text in the body of the wait page.

##Templates 

Your ``templates/`` directory will contain the templates for the HTML that gets displayed to the player.

oTree uses Django's [template system] (https://docs.djangoproject.com/en/dev/topics/templates/).

### Template blocks

Instead of having to write all your HTML from scratch, for example::

    <!DOCTYPE html>
    <html lang="en">
        <head>
        <!-- and so on... -->
    
You just have to define 2 blocks:

    {% block title %}
        Title goes here
    {% endblock %}
    
    {% block content %}
        Body HTML goes here.

        {% formrow form.contribution with label="What is your contribution?" %}

        {% next_button %}
    {% endblock %}

You may want to define your own base template rather than using oTree's built-in base template.
This is useful when you want to customize the appearance or functionality (e.g. by adding custom CSS or JavaScript), or customize the structure of HTML headings. This is easily done. Just edit the file `templates/global/Base.html`.

### Static files

You will likely want to include images, CSS, or even JavaScript in your pages.

To do that, put the following line in your template below the ``extends`` block:

    {% extends "Base.html" %}
    {% load staticfiles %}

And follow the [instructions here] (https://docs.djangoproject.com/en/dev/howto/static-files/).

## Additional tools

### Bootstrap

oTree comes with [Bootstrap] (http://getbootstrap.com/), a popular library for customizing a website's user interface.

You can use it if you want a [custom style] (http://getbootstrap.com/css/), or a [specific component] (http://getbootstrap.com/components/) like a table, alert, progress bar, label, etc. You can even make your page dynamic with elements like [popovers] (http://getbootstrap.com/javascript/#popovers), [modals] (http://getbootstrap.com/javascript/#modals), and [collapsible text] (http://getbootstrap.com/javascript/#collapse).

To use Bootstrap, usually you add a ``class=`` attributes to your HTML element.

For example, the following HTML will create a "Success" alert:

    <div class="alert alert-success">Great job!</div>

### HighCharts

oTree comes pre-loaded with [HighCharts](http://www.highcharts.com/demo). You can find examples in the library of how to use it.

To pass data like a list of values from Python to HighCharts, you can use the `otree.common.safe_json()` function. This converts to the correct JSON syntax and also uses "mark_safe" for the template.

Example:

    >>> a = [0, 1, 2, 3, 4, None]
    >>> safe_json(a)
    '[0, 1, 2, 3, 4, null]'


### jQuery

oTree comes pre-loaded with [jQuery](http://jquery.com/), a JavaScript library that lets you make your pages dynamic. You can include a script and reference the standard `$` variable.

### LaTeX


oTree comes pre-loaded with [KaTeX](http://khan.github.io/KaTeX/); you can insert LaTeX equations like this: `<span class="latex">1 + i = (1 + r)(1 + \pi)</span>`

##Smartphones and tablets
Since oTree uses Bootstrap for its user interface, your oTree app should work on all major browsers (Chrome/Internet Explorer/Firefox/Safari). When participants visit on a smartphone or tablet (e.g. iOS/Android/etc.), they should see an appropriately scaled down "mobile friendly" version of the site. This will generally not require much effort on your part since Bootstrap does it automatically, but if you plan to deploy your app to participants on mobile devices, you should test it out on a mobile device during development, since some HTML code doesn't look good on mobile devices.

## Groups

### Grouping and randomization

For the first round, the players are randomly split into groups of `Constants.players_per_group`. In subsequent rounds, By default, the groups chosen are kept the same for subsequent round. If you would like to change this, you can define the grouping logic in `Subsession.initialize`.

A group has a method `set_players` that takes as an argument a list of the players to assign to that group, in order. For example, if you want players to be reassigned to the same groups but to have roles randomly shuffled around within their groups (e.g. so player 1 will either become player 2 or remain player 1), you would do this:

    def initialize(self):
        if self.round_number > 1:
            for group in self.get_groups():
                players = group.get_players()
                players.reverse()
                group.set_players(players)

The subsession has a method `set_groups` that takes as an argument a list of lists, with each sublist representing a group. You can use this if your groups have uneven size. For example, if you have a session with 7 participants and want to split into a group of 2 and another group of the remaining 7, you could set `players_per_group = None` and instead do this:

    def initialize(self):
        if self.round_number == 1:
            players = self.get_players()
            g1 = players[:2]
            g2 = players[2:]
            self.set_groups([g1, g2])

[TODO: oTree should implement the most common grouping algorithms like stranger, perfect stranger, etc.]


## Treatments

If you want to assign participants to different treatment groups, you can put this code in the subsession's `initialize` method. For example, if you want some participants to have a blue background to their screen and some to have a red background, you would randomize as follows:

    def initialize(self):
        # randomize to treatments
        for player in self.get_players():
            player.color = random.choice(['blue', 'red'])

(To actually set the screen color you would need to pass `player.color` to some CSS code in the template, but that part is omitted here.)

If your game has multiple rounds, note that the above code gets executed for each round. So if you want to ensure that participants are assigned to the same treatment group each round, you should set the property at the participant level, which persists across subsessions, and only set it in the first round:

    def initialize(self):
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars['color'] = random.choice(['blue', 'red'])

Then, in the view code, you can access the participant's color with `self.player.participant.vars['color']`.

## Choosing which treatment to play

In the above example, players got randomized to treatments. This is useful in a live experiment, but when you are testing your game, it is often useful to choose explicitly which treatment to play. Let's say you are developing the game from the above example and want to show your colleagues both treatments (red and blue). You can create 2 session types in settings.py that have the same keys to session type dictionary , except the `treatment` key:

```
SESSION_TYPES =  
      [
        {
            'name':'my_game_blue',
            # other arguments...

            'treatment':'blue',

        },
        {
           'name':'my_game_red',
            # other arguments...
            'treatment':'red',
        },
     ]
```

Then in the `initialize` method, you can check which of the 2 session types it is:

    def initialize(self):
        for p in self.get_players():
            if 'treatment' in self.session.session_type:
                # demo mode
                p.color = self.session.session_type['treatment']
            else:
                # live experiment mode
                p.color = random.choice(['blue', 'red'])

Then, when someone visits your demo page, they will see the "red" and "blue" treatment, and choose to play one or the other. Of course, you can also have a third treatment that omits the `vars` argument and therefore randomizes participants to blue or red.


## Rounds

### Round numbers

Subsession objects have attributes `round_number`, which contains the current round number, starting from 1.

## Accessing data from previous rounds

Player objects have methods `in_previous_rounds()` and `in_all_rounds()` that returns a list of players representing the same participant in previous rounds of the same app. The difference is that `in_all_rounds()` includes the current round's player. For example, if you wanted to calculate a participant's payoff for all previous rounds of a game, plus the current one:

        cumulative_payoff = sum([p.payoff for p in self.player.in_all_rounds()])

Similarly, subsession objects have methods `in_previous_rounds()` and `in_all_rounds()` that work the same way.

## Accessing data from previous subsessions in different apps

The above method only works if the same app is repeated for multiple rounds. If you want to pass data between subsessions of different app types (e.g. the participant is in the questionnaire and needs to see data from their ultimatum game results), you should store this data in the participant object, which persists across subsessions. Each participant has a field called `vars`, which is a dictionary that can store any data about the player. For example, if you ask the participant's name in one subsession and you need to access it later, you would store it like this:

`self.player.participant.vars['first name'] = 'Chris'`

Then in a future subsession, you would retrieve this value like this:

`self.player.participant.vars['first name']` # returns 'Chris'

## Global variables

For session-wide globals, you can use `session.vars`,
either through `player.participant.session.vars` or `player.subsession.session.vars` (both are equivalent).

This is a dictionary just like `participant.vars`.

## Trying your app

You can launch your app on your local development machine to test it, and then when you are satisfied, you can deploy it to a server.

### Testing locally
You will be testing your app frequently during development, so that you can see how the app looks and feels and discover bugs during development.

To help with launching your app, there is a script in your project's root directory called `otree`. You can run it as follows:

    ./otree resetdb

This command will create your app in one command. It does the following:

* Delete your database (so be careful not to run this script unless you are OK with losing everything currently in the database)
* Set up a new blank database according to the schema in your app's `models.py` files

After running this script, open your PyCharm window and select "Run > Debug". Your app should be set to "Django server". When you launch it, a browser window will open to the demo page, where you can test your game. Click on a session name and you will get a start link for the experimenter, as well as the links for all the participants. You can open all the start links in different tabs and simulate playing as multiple participants simultaneously.

You can send the demo page link to your colleagues or publish it to a public audience. You can modify the `show_on_demo_page` attribute for your session in `settings.py` to control whether a given session is listed on the demo page. If you don't want a demo page at all, make this function return `False`.

### Debugging
Once you start playing your app, you will sometimes get a yellow Django error page with lots of details. To troubleshoot this, look at the error message and "Exception location" fields. If the exception location is somewhere outside of your app's code (like if it points to an installed module like Django or oTree), look through the "Traceback" section to see if it passes through your code. Once you have found a reference to a line of code in your app, go to that line of code and see if the error message can help you pinpoint an error in your code. Googling the error name or message will often take you to pages that explain the meaning of the error and how to fix it.

#### Debugging with PyCharm
PyCharm has an excellent debugger that you should be using continuously. You can insert a breakpoint into your code by clicking in the left-hand margin on a line of code. You will see a little red dot. Then reload the page and the debugger will pause when it hits your line of code. At this point you can inspect the state of all the local variables, execute print statements in the built-in intepreter, and step through the code line by line.

More on the PyCharm debugger [here](http://www.jetbrains.com/pycharm/webhelp/debugging.html).

## Test Bots

Automated tests are an essential part of building a oTree app. You can easily program a bot that simulates multiple players simultaneously playing your app.

Tests with dozens of bots complete with in seconds, and afterward automated tests can be run to verify correctness of the app (e.g. to ensure that payoffs are being calculated correctly).

This automated test system saves the programmer the effort of having to re-test the application every time something is changed.

### Launching tests
oTree tests entire sessions, rather that individual apps in isolation. This is to make sure the entire session runs, just as participants will play it in the lab.

Let's say you want to test the session named `ultimatum_game` in `settings.py`. To test, run the following command from your project's root directory:

    ./otree test ultimatum_game

This command will test the session, with the number of participants specified in `settings.py`. For example, `num_bots` is 30, then when you run the tests, 30 bots will be instantiated and will play concurrently.

To run tests for all sessions in `settings.py`, run:

    ./otree test

### Writing tests

Tests are contained in your app's `tests.py`. Fill out the `play_round()` method of your `PlayerBot` (and `ExperimenterBot` if you have experimenter pages). It should simulate each page submission. For example:

    self.submit(views.Start)
    self.submit(views.Offer, {'offer_amount': 50})

Here, we first submit the `Start` page, which does not contain a form. The next page is `Offer`, which contains a form whose field is called `offer_amount`, which we set to `50`. This is a way of automating the task of 

Your test bot must simulate playing the game correctly. The bot in the above example would raise an error if the page after `Start` was called `Instructions` rather than `Offer`, or if the field `offer_amount` was actually called something else. Your test bot is a specification of how you expect your app to work, so when it raises an error, it will alert you that your app is not behaving as intended.

Rather than programming many separate bots, you program one bot that can play any variation of the game. For example, if you have different treatment groups that play different pages, you can branch by checking a variable on the treatment. For example, here is how you would play if one treatment group sees a "threshold" page but the other treatment group should see an "accept" page:

        if self.group.threshold:
            self.submit(views.Threshold, {'offer_accept_threshold': 30})
        else:
            self.submit(views.Accept, {'offer_accepted': True})

If player 1 in a group sees different pages from player 2, you can define separate methods `play_p1()` and `play_p2()` and branch like this:

        if self.player.id_in_group == 0:
            self.play_p1()
        else:
            self.play_p2()

To get the maximal benefit, your bot should thoroughly test all parts of your code. Here are some ways you can test your app:

* Ensure that it correctly rejects invalid input. For example, if you ask the user to enter a number that is a multiple of 3, you can verify that entering 4 will be rejected by using the `submit_with_invalid_input` method as follows. This line of code will raise an error if the submission is _accepted_:

    `self.submit_with_invalid_input(views.EnterNumber, {'multiple_of_3': 4})`

* You can put assert statements in the bot's `validate_play()` method to check that the correct values are being stored in the database. For example, if a player's bonus is defined to be 100 minus their offer, you can check your program is calculating it correctly as follows:

    `self.submit(views.Offer, {'offer': 30})`

    `assert self.player.bonus == 70`

* You can use random amounts to test that your program can handle any type of random input:

    `self.submit(views.Offer, {'offer': random.randint(0,100)})`


Bots can either be programmed to simulate playing the game according to an ordinary strategy, or to test "boundary conditions" (e.g. by entering invalid input to see if the application correctly rejects it). Or yet the bot can enter random input on each page. 

If your app has [[Experimenter Pages]], you can also implement the `play` method on the `ExperimenterBot`.

## Money and Points 

In a typical lab experiment, participants are paid money at the end. Their payoffs may depend on how they played the games.

You can specify the payment currency in `settings.py`, by setting `PAYMENT_CURRENCY_CODE` to "USD", "EUR", "GBP", and so on. This means that all currency amounts the participants see will be automatically formatted in that currency, and at the end of the session when you print out the payments page, amounts will be displayed in that currency.

In oTree apps, currency values have their own data type. You can define a currency value with the `c()` function, e.g. `c(10)` or `c(0)`. Correspondingly, there is a special model field for currency values: `CurrencyField`. For example, each player has a `payoff` field, which is a `CurrencyField`. Currency values work just like numbers (you can do mathematical operations like addition, multiplication, etc), but when you pass them to an HTML template, they are automatically formatted as currency. For example, if you set `player.payoff = c(1.20)`, and then pass it to a template, it will be formatted as `$1.20` or `1,20 €`, etc., depending on your `PAYMENT_CURRENCY_CODE` and `LANGUAGE_CODE` settings.

Note: instead of using Python's built-in `range` function, you should use oTree's `currency_range` with currency values. For example, `currency_range(c(0), c(0.10), c(0.02))` returns something like:

```
[Money($0.00), Money($0.02), Money($0.04), Money($0.06), Money($0.08), Money($0.10)]
```

### Points
Sometimes it is preferable for players to play games not for real money but for points or "experimental currency units", which are converted to real money at the end of the session. You can set `USE_POINTS = True` in `settings.py`, and then in-game currency amounts will be expressed in points rather than real money.

For example, `c(10)` is displayed as `10 points`. You can specify the conversion rate to real money in `settings.py` by providing a `money_per_point` key in the session type dictionary. For example, if you pay the user 2 cents per point, you would set `money_per_point = 0.02`.

You can convert a point amount to money using the `to_money()` method,
which takes as an argument the current subsession
(this is necessary because subsessions in different apps can have different conversion rates).

Let's say `money_per_point = 0.02`

```
c(10) # evaluates to Currency(10 points)
c(10).to_money(self.subsession) # evaluates to $0.20
```

## Admin

oTree comes with an admin interface, so that experimenters can manage sessions, monitor the progress of live sessions, and export data after sessions.

Open your browser to the root url of your web application. If you're developing locally, this will be http://127.0.0.1:8000/. This will give you a login screen. Log in with the admin username and password specified in `settings.py`.


## Heroku

TODO: add content about

* add-ons (Sentry, PG backups)

### To create new remote:
```
heroku login  # if not yet
heroku create
git push heroku master
```

### To add an existing remote:

`heroku git:remote -a ancient-coast-2653

### Testing on Heroku

To recreate and push to Heroku, run this command:

```
git push myherokuapp master
./otree-heroku resetdb myherokuapp
```

Where `myherokuapp` is the name of your Heroku app `myherokuapp.herokuapp.com`

If it's a production website, you should set the environment variable `OTREE_PRODUCTION`, with:

`heroku config:set OTREE_PRODUCTION=1 --app myherokuapp`


## Server Setup

oTree can be deployed on your own server, or using a cloud service like Heroku. 

If you are not experienced with web server administration, Heroku may be a much simpler option for you, because Heroku automatically handles much of the configuration. Instructions on how to deploy oTree to Heroku are [[here|Heroku]].

Nevertheless, in various situations it will be preferable to run oTree on your own server. Reasons may include:

* You do not want your server to be accessed from the internet
* You will be launching your experiment in a setting where internet access is unavailable
* You want full control over how your server is configured

oTree runs on top of Django, so oTree setup is the same as Django setup. Django runs on a wide variety of servers, except getting it to run on Windows may require extra work. 

The most typical setup will be a Linux server with Apache. The instructions for this setup are [here](https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/modwsgi/).

If you have been developing your project on your local PC, you should push your oTree folder to your webserver, e.g. with Git. Then, you should make sure your webserver has Python installed (possibly in a `virtualenv`), and do `pip install -r requirements.txt` to install all the dependencies. When you are ready to launch the experiment, you should set `OTREE_PRODUCTION` to `1`, to turn off `DEBUG` mode.

## Database setup

We generally recommend using PostgreSQL as your production database. You can create your database with a command like this:

`psql -c 'create database django_db;' -U postgres`

Then, you should set the following environment variable, so that it can be read by `dj_database_url`:

`DATABASE_URL=postgres://postgres@localhost/django_db`

## Lab Experiments 

### Creating sessions

Create a session in the admin.
[TODO: more info]

### Opening links

To launch a session, each participant must open their link. There are 2 options for how to open URLs.

#### Lab

In the admin interface, go to the "global data" section, and copy the "lab link". This is a permanent URL that will last as long as you use the same server [TODO: finish]

Each workstation has a permanent URL that, when clicked, will route the participant to the currently active session.


choose an active session from the dropdown. Then, copy 


#### Unique URLs




If you are running your experiment in a lab, you should deploy the links to the target workstations using whatever means is available to you. If you have a tool that can push distinct URLs to each PC in the lab, you can use that. Or you can set up a unique email account for each workstation, and then send the unique links to PCs using a mail merge. Then open the link on each PC.

#### Player labels
oTree uses a unique code to identify each participant. However, you can assign each session participant a "label" that can be any convenient way to identify them to you, such as:

* Name
* Computer workstation number
* Email address
* ID number

This label will be displayed in places where participants are listed, like the oTree admin interface or the payments page.

You can assign each participant a label by adding a parameter to each start link.
For example, if you want to assign a participant the label "WORKSTATION_1", you would take the start link for that participant:

    http://[participant's unique link]?some_param=1

And change it to:

    http://[participant's unique link]?some_param=1&participant_label=WORKSTATION_1

Outside of oTree, you can create a script that adds a unique `participant_label` to each start link as indicated above. Then, when the link is opened, the oTree server will register that participant label for that participant.

### Monitor sessions
While your session is ongoing, you can monitor the live progress in the admin interface. The admin tables update live, highlighting changes as they occur. The most useful table to monitor is "Session participants", which gives you a summary of all the participants' progress. You can also click the "participants" table of each app to see the details of all the data being entered in your subsessions.

## Online experiments

Experiments can be launched to participants playing over the internet, in a similar way to how experiments are launched the lab. Login to the admin, create a session, then distribute the links to participants via email or a website.

In a lab, you usually can start all participants at the same time, but this is often not possible online, because some participants might click your link hours after other participants. If your game requires players to play in groups, you may want to set the `group_by_arrival_time` key in  session type dictionary to `True`. This will group players in the order in which they arrive to your site, rather than randomly, so that players who arrive around the same time play with each other.

## For Django Devs

## Guidelines for developers contributing to oTree's library of games

### Keep it simple
The purpose of the oTree sample games library is to show examples so that new users can understand how to do things in oTree. They will then copy-paste these code snippets when they create their own apps. So, we want a consistent coding style in the oTree library, especially because many users will be novice Python programmers. In general we should avoid complex code and algorithms. We should also try to avoid code that relies on less commonly used Python/Django features or "tricks"/hacks. Even if it works nicely in a particular context, these risk causing confusion when someone copies them without really understanding.

Examples of code that could confuse a newcomer:
* Using `a[::-1]` to reverse a list (not obvious what this is doing, and hard to Google
* Decorators like `@property` or `@staticmethod`
* Using class inheritance within your app (e.g. subclassing one view from another, other than subclassing oTree's built-in views)
* Use lists instead of tuples, because when a tuple only has 1 element you have to remember the (comma,)

### Consistency
* Don't delete unused imports in the <standard imports> section; a user should always be able to rely on those being there.

### Don't repeat yourself
* If a certain page is being repeated in multiple apps, it may be better suited as a separate app that gets added to `app_sequence` for each session in `settings.py`. Examples: surveys and feedback pages.
* You should obey to Django's "Don't repeat yourself" principle: "Every distinct concept and/or piece of data should live in one, and only one, place. Redundancy is bad."
 * Numeric constants, even simple ones like 0.5 or 3, should go in the `Constants` class

### Separate logic from presentation
* User-facing strings should be defined in the template wherever possible. This is to keep a separation between logic and UI, which makes it easier for a non-programmer to modify a string, since they only have to look at the HTML. Also, in the template, strings are displayed in context, whereas if they are defined in Python code, they are usually out of context.
* Try not to put much logic in templates. It makes it hard for a non-programmer to understand and edit the template, and anyways logic in templates is often more verbose and harder to debug.

## Intro to oTree for Django developers

### Differences between oTree and Django

#### Models
* Field labels should go in the template formrow, rather than the model field's `verbose_name`.
* `null=True` and `default=None` are not necessary in your model field declarations; in oTree fields are null by default.
* On `CharField`s, `max_length` is not required.

## Kiosk Mode 

During an experiment, subjects are expected to stay on the given pages/game, instead of browsing irrelevant websites or using other applications. Kiosk mode locks down the oTree pages on a web browser thus allows the subjects to focus. Here we provide some guidelines to initiate Kiosk mode with different browsers/on various systems. In general, Kiosk mode is rather user-friendly so one can easily search online how to use it on specific platforms.

#### iOS (iPhone/iPad)

1. Go to Setting – Accessibility – Guided Access
1. Turn on Guided Access and set a passcode for your Kiosk mode
1. Open your web browser and enter your URL
1. Triple-click home button to initiate Kiosk mode
1. Circle areas on the screen to disable (e.g. URL bar) and activate

#### Android

There are several apps for using Kiosk mode on Android, for instance: [Kiosk Browser Lockdown](https://play.google.com/store/apps/details?id=com.procoit.kioskbrowser&hl=en).

![](http://i.imgur.com/VJ72fKv.png)

For iOS and Android tablets, Kiosk mode will continue to function after normal restart. However, if subjects enter Android safe mode, the app can be disabled.

#### Chrome on PC
1. Go to Setting – Users – Add new user
1. Create a new user with a desktop shortcut
1. Right-click the shortcut and select “Properties”
1. In the “Target” filed, add to the end either ```--kiosk "http://www.your-otree-server.com"``` or ```--chrome-frame  --kiosk "http://www.your-otree-server.com"```
1. Disable hotkeys (see [here](http://superuser.com/questions/727072/what-windows-shortcuts-should-be-blocked-on-a-kiosk-mode-pc))
1. Open the shortcut to activate Kiosk mode

#### IE on PC
IE on PC
See [here](http://support2.microsoft.com/kb/154780)

#### Mac
There are several apps for using Kiosk mode on Mac, for instance: [eCrisper](http://ecrisper.com/). Mac keyboard shortcuts should be disabled.


## Payment PDF

At the end of your session, you can open and print a page that lists all the participants and how much they should be paid. This is in the Sessions table, in the "payments page" column.

![](http://i.imgur.com/nSMlWcY.png)

## Export Data

You can download your raw data in text format (CSV) so that you can view and analyze it with a program like Excel, Stata, or R. Go to the "Export data" table and choose your app.

You can also download a documentation file for each app, which explains the meaning of the different variable names. It is auto-generated from your source code. Whatever you specify in a model field's `doc=` argument will show up here.

## AMT Integration

## Overview
oTree provides integration with <strong><a href="https://www.mturk.com/mturk/welcome" target="_blank">Amazon Mechanical Turk (AMT)</a></strong>. oTree authenticates users visiting from the AMT service, and then sends payments to the correct AMT account. Researchers, however, must have an employer account with AMT, which currently requires a U.S. address and bank account.
## Session for AMT
Login to oTree admin panel and create new session:

![Create session](http://i.imgur.com/oXr33PU.png)

Set the session open and copy html snippet to your AMT HIT page:

![HTML snippet](http://i.imgur.com/gxoz3hh.png)

## AWS credentials
To make payments to participants you need to generate
`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
[here](https://console.aws.amazon.com/iam/home?#security_credential):

![AWS key](http://i.imgur.com/dNhkOiA.png)

On heroku add generated values to your environment variables:

    heroku config:set AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID --app=YOUR_APP_NAME
    heroku config:set AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY --app=YOUR_APP_NAME

## Payment

    heroku run "./otree mturk_pay SESSION_ID" --app=YOUR_APP_NAME
    

## Debug Info

Any application can be run so that that debug information is displayed on the bottom of all screens. The debug information consists of the ID in group, the group, the player, the participant label, and the session code. The session code and participant label are two randomly generated alphanumeric codes uniquely identifying the session and participant. The ID in group identies the role of the player (e.g., in a principal-agent game, principals
might have the ID in group 1, while agents have 2).

![](http://i.imgur.com/DZsyhQf.png)

##Progress-Monitor 

The progress monitor allows the researcher to monitor the progress of an experiment. It features a display that can be **filtered** and **sorted**, for example by computer name or group. The experimenter can see the progress of all participants, including their current action and taken decisions. Updates are shown as they happen **in real time** and cells that change are highlighted in yellow. Because the progress monitor is web-based, **multiple collaborators can simultaneously open it on several devices on premises or at remote locations**. 

![](http://i.imgur.com/0nYKnDp.png)


## Session Interface  

The session interface is an optional feature convenient in some experiments. In many experimental settings, in addition to monitoring, **an experimenter needs to receive instructions or provide input for the experiment**. The session interface can instruct an experimenter on what to do next and show text to be read aloud. The session interface can also request input from the experimenter at a specic point in the session. For example, in an Ellsberg experiment, the experimenter might roll an opaque urn prior to the session; the session interface will remind the experimenter to show the urn to the participants, tell the experimenter when all participants have selected their bets, and instruct her to draw a ball from the urn. It will then ask the drawn color, so that oTree can calculate participants' payoffs.


## User Input Validation

If a participant does not fill out a required form or submits an invalid value, the form is automatically re-displayed, highlighting and explaining the user's error. The experimenter can specify what answers are valid; in the case of a numeric input field, the experimenter could also specify valid numbers/ranges. Validation is only intended for cases where the experimenter wants to prevent the participant from proceeding without making an answer satisfying some specified criteria.

_Example 1:_
![](http://i.imgur.com/Sz34h7d.png)

_Example 2:_
![](http://i.imgur.com/BtG8ZHX.png)

