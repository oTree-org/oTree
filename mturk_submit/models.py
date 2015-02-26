# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json

# </standard imports>

author = 'Your name here'

# The description of the app support HTML tags
doc = """
Your <a href="http://otree.org" target="_blank">oTree</a> app description
"""

# Link of the source code of your app or empty
source_code = "https://github.com/oTree-org/oTree/"


# List of strings of recomended literature for this app or an empty list
bibliography = (
    (
        'Basar, T., Olsder, G. J., Clsder, G. J., Basar, T., Baser, T., & '
        'Olsder, G. J. (1995). Dynamic noncooperative game theory (Vol. 200). '
        'London: Academic press.'
    ),
    (
        'Harsanyi, J. C., & Selten, R. (1988). A general theory of '
        'equilibrium selection in games. MIT Press Books, 1.'
    )
)


# Resources for understand your app, normally a wikipedia articles
# or an empty dict (This will be sorted alphabetically)
links = {
    "Wikipedia": {
        "Game Theory": "http://en.wikipedia.org/wiki/Game_theory",
        "Nash Equilibrim": "http://en.wikipedia.org/wiki/Nash_equilibrium"
    },
    "Resources": {
        "Introduction to Game Theory [Video]":
                "https://www.youtube.com/watch?v=nM3rTU927io",
    }
}


# A list of relevant keywords for your app or an empty list. This keyword will
# be automatically linked with duckduckgo.com anonymous search
keywords = ("Game Theory", "Nash Equilibrium", "Economics")


class Constants:
    name_in_url = 'mturk_submit'
    players_per_group = 2
    num_rounds = 1

    # define more constants here


class Subsession(otree.models.BaseSubsession):
    pass


class Group(otree.models.BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def set_payoffs(self):
        for p in self.get_players():
            p.payoff = 0 # change to whatever the payoff should be


class Player(otree.models.BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>

    def other_player(self):
        """Returns other player in group. Only valid for 2-player groups."""
        return self.get_others_in_group()[0]

    # example field
    my_field = models.CurrencyField(
        min=c(0),max=c(10),
        doc="""
        Description of this field, for documentation
        """
    )


    def role(self):
        # you can make this depend of self.id_in_group
        return ''
