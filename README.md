## Live demo
http://demo.otree.org/

## Homepage
http://www.otree.org/

## About

oTree is a Django-based framework that makes it easy to implement multiplayer decision strategy games.  
Many of the details of writing a web application are abstracted away, 
meaning that the code is focused on the logic of the game,
and oTree programming is accessible to programmers without advanced experience in web app development.

See the live demo [here](http://demo.otree.org/).

This repository contains the games; the oTree core libraries are [here](https://github.com/oTree-org/otree-core).

## Quick start
After forking & cloning the repo:

    pip install -r requirements_base.txt
    ./otree resetdb
    ./otree runserver

## Documentation
https://github.com/oTree-org/oTree/wiki

## Contact
chris@otree.org (you can also add me on Skype by searching this email address; please mention oTree in your contact request)

Please contact me if you find any bugs or issues in oTree.

## Prerequisites

This page is written for people who may not have Python development experience, and covers the basics of the command line, Python, pip, and an IDE. If you know about these tools, you can skip this page.

## Basic understanding of command line

You need a basic understanding of your operating system's command prompt (Terminal on Mac, or PowerShell on Windows), like ``ls``, ``cd``, ``mv``, and ``sudo``.

## Python installation
You will write your oTree apps in [Python](http://www.python.org/).

### Installation

#### Python interpreter

Install [Python](http://www.python.org/) version 2.7 (not 3.X).

On Windows, select the option to add Python to your PATH while installing.

On Mac/Unix, it is very likely that Python is already installed. Open the Terminal and write ``python`` and hit Enter. If you get something like `-bash: python: command not found` you will have to install it yourself.

#### Pip

You will need a program called Pip in order to install packages.

Then, download [get-pip.py](https://raw.github.com/pypa/pip/master/contrib/get-pip.py).

On Windows, right-click the Windows PowerShell app icon, then click "Run as administrator" and run this command:

`python get-pip.py`

On Mac/Unix, run:

`sudo python get-pip.py`

You will be asked to enter the admin password.


## PyCharm

To ease the learning curve of oTree, we strongly recommend using [PyCharm Professional](http://www.jetbrains.com/pycharm/), even though there are many other good editors for Python code. This is because:

* PyCharm has features that make oTree/Django development easier
* oTree has special integration with PyCharm's code completion functionality
* This documentation gives instructions assuming you are using PyCharm
* oTree has been thoroughly tested with PyCharm

If you are a student, teacher, or professor, PyCharm Professional is [free](https://www.jetbrains.com/student/). Note: we recommend PyCharm Professional rather than PyCharm Community Edition.


_TODO:_
* runserver & debug


## Setup

## Choose a location for your oTree work

Choose where on your computer you want to store your oTree work.
It can be anywhere, like a folder in "My Documents" or "Documents".

## Fork our repository

Create a GitHub account if you don't have one.

Install Git:
* On Windows, install [msysgit](http://msysgit.github.io/) (during installation, select the option to add git to your path)
* [TODO: Mac]

Go to https://github.com/oTree-org/otree, and in the top-right corner of the page, click Fork.

## Clone the repository

Right now, you have a fork of the oTree repository on GitHub, but you don't have the files in that repository on your computer. Let's create a clone of your fork locally on your computer.

1. On GitHub, navigate to your fork of the oTree repository.
2. In the right sidebar of your fork's repository page, copy the clone URL for your fork.
3. Open Terminal (for Mac and Linux users) or the command line (for Windows users).
4. Go to the folder on your PC where you want to work on oTree (the next command will create an `oTree` folder here)
4. Enter `git clone https://github.com/YOUR-USERNAME/oTree.git` 
5. Enter `git remote add upstream https://github.com/oTree-org/oTree.git`

## Install dependencies
Change into the `oTree` directory (the one containing `requirements_base.txt`), and run the following command:

`pip install -r requirements_base.txt`

## Create the database

Run the following command (which creates the database):

`./otree resetdb`
	
## Test that it worked

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

##Sessions

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

You can define your session's properties in `sessions.py`. Here are the parameters for the above example:

    SessionType(
        name='my_session',
        fixed_pay=1000,
        app_sequence=['trust', 'ultimatum', 'questionnaire'],
    )        

## Players vs. participants

The terms "player" and "participant" mean similar things but are slightly different.

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
