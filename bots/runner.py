from typing import List
import logging
from collections import OrderedDict, defaultdict
from pathlib import Path
from django.conf import settings
import pytest

import otree.session
import otree.common_internal

from .bot import ParticipantBot
import datetime
import os
import codecs
import otree.export
from otree.constants_internal import AUTO_NAME_BOTS_EXPORT_FOLDER
from otree.models_concrete import ParticipantToPlayerLookup
from otree.models import Session, Participant
from otree.session import SESSION_CONFIGS_DICT

logger = logging.getLogger(__name__)


class SessionBotRunner:
    def __init__(self, bots: List[ParticipantBot]):
        self.bots = OrderedDict()

        for bot in bots:
            self.bots[bot.participant_id] = bot

    def play(self):
        '''round-robin'''
        self.open_start_urls()
        loops_without_progress = 0
        while True:
            if len(self.bots) == 0:
                return
            # bots got stuck if there's 2 wait pages in a row
            if loops_without_progress > 10:
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
                        bot.submit(**submission)
                        progress_made = True
            if not progress_made:
                loops_without_progress += 1

    def open_start_urls(self):
        for bot in self.bots.values():
            bot.open_start_url()


def make_bots(*, session_pk, case_number, use_browser_bots) -> List[ParticipantBot]:
    update_kwargs = {'_is_bot': True}
    if use_browser_bots:
        update_kwargs['is_browser_bot'] = True

    Participant.objects.filter(session_id=session_pk).update(**update_kwargs)
    bots = []

    # can't use .distinct('player_pk') because it only works on Postgres
    # this implicitly orders by round also
    lookups = ParticipantToPlayerLookup.objects.filter(
        session_pk=session_pk).order_by('page_index')

    seen_players = set()
    lookups_per_participant = defaultdict(list)
    for lookup in lookups:
        player_identifier = (lookup.app_name, lookup.player_pk)
        if not player_identifier in seen_players:
            lookups_per_participant[lookup.participant_code].append(lookup)
            seen_players.add(player_identifier)

    for participant_code, lookups in lookups_per_participant.items():
        bot = ParticipantBot(lookups=lookups, case_number=case_number)
        bots.append(bot)

    return bots


def run_bots(session: Session, case_number=None):
    bot_list = make_bots(
        session_pk=session.pk, case_number=case_number, use_browser_bots=False
    )
    runner = SessionBotRunner(bots=bot_list)
    runner.play()

# i used to use @pytest.mark.filterwarnings('ignore', category=RemovedInDjango20Warning)
# but easier to use --disable-warnings to make sure they're all gone
# function name needs to start with "test" for pytest to discover it
# in this module
@pytest.mark.django_db(transaction=True)
def test_all_bots_for_session_config(
        session_config_name, num_participants, export_path):
    """
    this means all configs and test cases are in 1 big test case.
    so if 1 fails, the others will not get run.
    to separate them, we would need to move some of this code
    to pytest_generate_tests in conftest.py
    """
    if session_config_name:
        session_config_names = [session_config_name]
    else:
        session_config_names = SESSION_CONFIGS_DICT.keys()

    for config_name in session_config_names:
        try:
            config = SESSION_CONFIGS_DICT[config_name]
        except KeyError:
            # important to alert the user, since people might be trying to enter app names.
            raise Exception(f"No session config with name '{config_name}'.") from None

        bot_modules = [f'{app_name}.tests' for app_name in config['app_sequence']]
        pytest.register_assert_rewrite(*bot_modules)

        num_bot_cases = config.get_num_bot_cases()
        for case_number in range(num_bot_cases):
            logger.info("Creating '{}' session (test case {})".format(
                config_name, case_number))

            session = otree.session.create_session(
                session_config_name=config_name,
                num_participants=(num_participants or config['num_demo_participants']),
            )

            run_bots(session, case_number=case_number)
            logger.info('Bots completed session')
    if export_path:

        now = datetime.datetime.now()

        if export_path == AUTO_NAME_BOTS_EXPORT_FOLDER:
            # oTree convention to prefix __temp all temp folders.
            export_path = now.strftime('__temp_bots_%b%d_%Hh%Mm%S.%f')[:-5] + 's'

        os.makedirs(export_path, exist_ok=True)


        for app in settings.INSTALLED_OTREE_APPS:
            model_module = otree.common_internal.get_models_module(app)
            if model_module.Player.objects.exists():
                fpath = Path(export_path, "{}.csv".format(app))
                with fpath.open("w", encoding="utf8") as fp:
                    otree.export.export_app(app, fp, file_extension='csv')
        fpath = Path(export_path, "all_apps_wide.csv")
        with fpath.open("w", encoding="utf8") as fp:
            otree.export.export_wide(fp, 'csv')

        logger.info('Exported CSV to folder "{}"'.format(export_path))
