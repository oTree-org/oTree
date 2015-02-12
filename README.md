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

