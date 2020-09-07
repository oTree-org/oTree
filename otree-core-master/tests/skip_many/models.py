# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

from otree.api import BaseSubsession, BaseGroup, BasePlayer, BaseConstants
# </standard imports>


doc = "foo"


class Constants(BaseConstants):
    name_in_url = 'skip_many'
    players_per_group = 2
    num_rounds = 5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
