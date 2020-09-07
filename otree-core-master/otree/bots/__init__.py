#!/usr/bin/env python
# -*- coding: utf-8 -*-

# NOTE: this imports the following submodules and then subclasses several
# classes importing is done via import_module rather than an ordinary import.
#
# The only reason for this is to hide the base classes from IDEs like PyCharm,
# so that those members/attributes don't show up in autocomplete,
# including all the built-in django fields that an ordinary oTree programmer
# will never need or want. if this was a conventional Django project I wouldn't
# do it this way, but because oTree is aimed at newcomers who may need more
# assistance from their IDE, I want to try this approach out.
#
# This module is also a form of documentation of the public API.

# 2016-07-18: not using the import_module trick for now, because currently,
# the PlayerBot class doesn't have any methods we need to hide
# from importlib import import_module
# otree_bot = import_module('otree.bots.bot')

from importlib import import_module

_bot_module = import_module('otree.bots.bot')

Bot = _bot_module.PlayerBot
Submission = _bot_module.Submission
SubmissionMustFail = _bot_module.SubmissionMustFail
