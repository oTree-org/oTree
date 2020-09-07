#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import six

from django.core.management.base import BaseCommand

from otree.session import create_session
from otree.room import ROOM_DICT


# =============================================================================
# LOGGING
# =============================================================================

logger = logging.getLogger('otree')


# =============================================================================
# COMMAND
# =============================================================================

class Command(BaseCommand):
    help = "oTree: Create a session."

    def add_arguments(self, parser):
        parser.add_argument(
            'session_config_name', type=six.u, help="The session config name")
        parser.add_argument(
            'num_participants', type=int,
            help="Number of participants for the created session")
        parser.add_argument(
            "-l", "--label", action="store", type=six.u,
            dest="label", default='', help="label for the created session")
        parser.add_argument(
            "--room", action="store", type=six.u,
            dest="room", default=None,
            help="Name of room to create the session in")

    def handle(self, *args, **options):
        session_config_name = options["session_config_name"]
        num_participants = options["num_participants"]
        label = options['label']

        session = create_session(
            session_config_name=session_config_name,
            num_participants=num_participants, label=label)

        if options['room']:
            room = ROOM_DICT[options['room']]
            room.session = session
            logger.info("Created session with code {} in room '{}'\n".format(
                session.code, options['room']))
        else:
            logger.info("Created session with code {}\n".format(session.code))
