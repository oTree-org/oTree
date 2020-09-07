#!/usr/bin/env python
# -*- coding: utf-8 -*-

from importlib import import_module

from django.db.models.signals import class_prepared

from otree.db.models import *  # noqa


# NOTE: this imports the following submodules and then subclasses several
# classes importing is done via import_module rather than an ordinary import.
# The only reason for this is to hide the base classes from IDEs like PyCharm,
# so that those members/attributes don't show up in autocomplete,
# including all the built-in django model fields that an ordinary oTree
# programmer will never need or want. if this was a conventional Django
# project I wouldn't do it this way, but because oTree is aimed at newcomers
# who may need more assistance from their IDE, I want to try this approach out.
# this module is also a form of documentation of the public API.

subsession_module = import_module('otree.models.subsession')
group_module = import_module('otree.models.group')
player_module = import_module('otree.models.player')


# so that oTree users don't see internal details
session_module = import_module('otree.models.session')
participant_module = import_module('otree.models.participant')


def ensure_required_fields(sender, **kwargs):
    """
    Some models need to hook up some dynamically created fields. They can be
    created on the fly or might be defined by the user in the app directly.

    We use this signal handler to ensure that these fields exist and are
    created on demand.
    """
    if hasattr(sender, '_ensure_required_fields'):
        sender._ensure_required_fields()


class_prepared.connect(ensure_required_fields)


Session = session_module.Session
Participant = participant_module.Participant
BaseSubsession = subsession_module.BaseSubsession
BaseGroup = group_module.BaseGroup
BasePlayer = player_module.BasePlayer
