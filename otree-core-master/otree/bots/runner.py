#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
from collections import OrderedDict
import mock

from django.db.migrations.loader import MigrationLoader
import pytest
import sys

import otree.session

from .bot import ParticipantBot


logger = logging.getLogger(__name__)


class SessionBotRunner(object):
    def __init__(self, bots, session_code):
        self.bots = OrderedDict()

        for bot in bots:
            self.bots[bot.participant.id] = bot

    def play_until_end(self):
        '''round-robin'''
        loops_without_progress = 0
        while True:
            if len(self.bots) == 0:
                print('Bots done!')
                return
            if loops_without_progress > 2:
                raise AssertionError('Bots got stuck')
            # store in a separate list so we don't mutate the iterable
            playable_ids = list(self.bots.keys())
            progress_made = False
            for pk in playable_ids:
                bot = self.bots[pk]
                if bot.on_wait_page():
                    pass
                else:
                    try:
                        submission = next(bot.submits_generator)
                    except StopIteration:
                        # this bot is finished
                        self.bots.pop(pk)
                        progress_made = True
                    else:
                        bot.submit(submission)
                        progress_made = True
            if not progress_made:
                loops_without_progress += 1


@pytest.mark.django_db(transaction=True)
def test_bots(session_config_name, num_participants, preserve_data):
    config_name = session_config_name
    session_config = otree.session.SESSION_CONFIGS_DICT[config_name]

    # num_bots is deprecated, because the old default of 12 or 6 was too
    # much, and it doesn't make sense to
    if num_participants is None:
        num_participants = session_config['num_demo_participants']

    num_bot_cases = session_config.get_num_bot_cases()
    for case_number in range(num_bot_cases):
        if num_bot_cases > 1:
            logger.info("Creating '{}' session (test case {})".format(
                config_name, case_number))
        else:
            logger.info("Creating '{}' session".format(config_name))

        session = otree.session.create_session(
            session_config_name=config_name,
            num_participants=num_participants,
            use_cli_bots=True, label='{} [bots]'.format(config_name),
            bot_case_number=case_number
        )
        bots = []

        for participant in session.get_participants():
            bot = ParticipantBot(participant)
            bots.append(bot)
            bot.open_start_url()

        bot_runner = SessionBotRunner(bots, session.code)
        bot_runner.play_until_end()


def run_pytests(**kwargs):

    session_config_name = kwargs['session_config_name']
    num_participants = kwargs['num_participants']
    preserve_data = kwargs['preserve_data']
    verbosity = kwargs['verbosity']

    this_module = sys.modules[__name__]

    # '-s' is to see print output
    argv = [this_module.__file__, '-s']
    if verbosity == 0:
        argv.append('--quiet')
    if verbosity == 2:
        argv.append('--verbose')

    if session_config_name:
        argv.extend(['--session_config_name', session_config_name])
    if num_participants:
        argv.extend(['--num_participants', num_participants])
    if preserve_data:
        argv.append('--preserve_data')

    # same hack as in resetdb code
    # because this method uses the serializer
    # it breaks if the app has migrations but they aren't up to date
    with mock.patch.object(
            MigrationLoader,
            'migrations_module',
            return_value='migrations nonexistent hack'
    ):

        return pytest.main(argv)
