#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import sys
from functools import reduce
from collections import OrderedDict
from decimal import Decimal
import warnings

import six
from six.moves import range
from six.moves import zip

from django.conf import settings
from django.db import transaction
from django.db.utils import OperationalError

import schema

import otree.db.idmap
from otree.models import Participant, Session
from otree.deprecate import OtreeDeprecationWarning
from otree.common_internal import (
    get_models_module, get_app_constants, validate_identifier,
    min_players_multiple, get_bots_module)
import otree.common_internal
from otree.common import RealWorldCurrency
from otree.models_concrete import ParticipantLockModel
import otree.bots.browser


def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)


def lcmm(*args):
    """Return lcm of args."""
    return reduce(lcm, args)


class SessionConfig(dict):

    def get_lcm(self):
        min_multiple_list = []
        for app_name in self['app_sequence']:
            app_constants = get_app_constants(app_name)
            # if players_per_group is None, 0, etc.
            min_multiple = min_players_multiple(
                app_constants.players_per_group)
            min_multiple_list.append(min_multiple)
        return lcmm(*min_multiple_list)

    def get_num_bot_cases(self):
        num_cases = 1
        for app_name in self['app_sequence']:
            bots_module = get_bots_module(app_name)
            cases = bots_module.PlayerBot.cases
            num_cases = max(num_cases, len(cases))
        return num_cases

    def validate(self):

        config_schema = schema.Schema({
            'name': str,
            'app_sequence': list,
            'participation_fee': object,
            'real_world_currency_per_point': object,
            'num_demo_participants': int,
            'doc': str,
            object: object,
        })

        try:
            config_schema.validate(self)
        except schema.SchemaError as e:
            raise ValueError('settings.SESSION_CONFIGS: {}'.format(e))

        validate_identifier(
            self['name'],
            identifier_description='settings.SESSION_CONFIG name'
        )

        app_sequence = self['app_sequence']
        if len(app_sequence) != len(set(app_sequence)):
            msg = (
                'settings.SESSION_CONFIGS: '
                'app_sequence of "{}" '
                'must not contain duplicate elements. '
                'If you want multiple rounds, '
                'you should set Constants.num_rounds.')
            raise ValueError(msg.format(self['name']))

        if len(app_sequence) == 0:
            raise ValueError(
                'settings.SESSION_CONFIGS: Need at least one subsession.')

        self.setdefault('display_name', self['name'])
        self.setdefault('doc', '')

        # TODO: fixed_pay is deprecated as of 2015-05-07,
        # in favor of participation_fee. make this required at some point.
        if (('participation_fee' not in self) and
                ('fixed_pay' in self)):
            warn_msg = (
                "'fixed_pay' is deprecated; "
                "you should rename it to 'participation_fee'.")
            warnings.warn(warn_msg, OtreeDeprecationWarning)

            self['participation_fee'] = self['fixed_pay']

        self['participation_fee'] = RealWorldCurrency(
            self['participation_fee'])

        # normalize to decimal so we can do multiplications, etc
        # quantize because the original value may be a float,
        # which when converted to Decimal may have some 'decimal junk'
        # like 0.010000000000000000208166817...
        self['real_world_currency_per_point'] = Decimal(
            self['real_world_currency_per_point']
        ).quantize(Decimal('0.00001'))

    def get_info(self):
        app_sequence = []
        for app_name in self['app_sequence']:
            models_module = get_models_module(app_name)
            num_rounds = models_module.Constants.num_rounds
            formatted_app_name = otree.common_internal.app_name_format(
                app_name)
            if num_rounds > 1:
                formatted_app_name = '{} ({} rounds)'.format(
                    formatted_app_name, num_rounds)
            subsssn = {
                'doc': getattr(models_module, 'doc', ''),
                'bibliography': getattr(models_module, 'bibliography', []),
                'name': formatted_app_name}
            app_sequence.append(subsssn)

        return {
            'doc': self['doc'],
            'app_sequence': app_sequence,
            'name': self['name'],
            'display_name': self['display_name'],
            'lcm': self.get_lcm()}


def get_session_configs_dict():
    SESSION_CONFIGS_DICT = OrderedDict()
    for config_dict in settings.SESSION_CONFIGS:
        config_obj = SessionConfig(settings.SESSION_CONFIG_DEFAULTS)
        config_obj.update(config_dict)
        config_obj.validate()
        SESSION_CONFIGS_DICT[config_dict['name']] = config_obj
    return SESSION_CONFIGS_DICT

SESSION_CONFIGS_DICT = get_session_configs_dict()


def app_labels_from_sessions(config_names):
    apps = set()
    for config_name in config_names:
        config = SESSION_CONFIGS_DICT[config_name]
        apps.update(config["app_sequence"])
    return apps


def create_session(
        session_config_name, label='', num_participants=None,
        _pre_create_id=None,
        room_name=None, for_mturk=False, use_cli_bots=False,
        is_demo=False, force_browser_bots=False,
        honor_browser_bots_config=False, bot_case_number=None):

    session = None
    use_browser_bots = False
    num_subsessions = 0

    with transaction.atomic():
        # 2014-5-2: i could implement this by overriding the __init__ on the
        # Session model, but I don't really know how that works, and it seems
        # to be a bit discouraged: http://goo.gl/dEXZpv
        # 2014-9-22: preassign to groups for demo mode.

        otree.db.idmap.activate_cache()

        try:
            session_config = SESSION_CONFIGS_DICT[session_config_name]
        except KeyError:
            msg = 'Session config "{}" not found in settings.SESSION_CONFIGS.'
            raise ValueError(msg.format(session_config_name))

        if force_browser_bots:
            use_browser_bots = True
        elif (session_config.get('use_browser_bots') and
              honor_browser_bots_config):
            use_browser_bots = True
        else:
            use_browser_bots = False
        if use_browser_bots and bot_case_number is None:
            # choose one randomly
            num_bot_cases = session_config.get_num_bot_cases()
            # choose bot case number randomly...maybe reconsider this?
            # we can only run one.
            bot_case_number = random.choice(range(num_bot_cases))

        session = Session.objects.create(
            config=session_config,
            label=label,
            _pre_create_id=_pre_create_id,
            use_browser_bots=use_browser_bots,
            is_demo=is_demo,
            _bot_case_number=bot_case_number)

        def bulk_create(model, descriptions):
            model.objects.bulk_create([
                model(session=session, **description)
                for description in descriptions])
            return model.objects.filter(session=session).order_by('pk')

        # check that it divides evenly
        session_lcm = session_config.get_lcm()
        if num_participants % session_lcm:
            msg = (
                'Session Config {}: Number of participants ({}) does not '
                'divide evenly into group size ({})'
            ).format(session_config['name'], num_participants, session_lcm)
            raise ValueError(msg)

        if for_mturk:
            session.mturk_num_participants = (
                    num_participants /
                    settings.MTURK_NUM_PARTICIPANTS_MULTIPLE)

        start_order = list(range(num_participants))
        if session_config.get('random_start_order'):
            random.shuffle(start_order)

        participants = bulk_create(
            Participant,
            [{
                'id_in_session': id_in_session,
                'start_order': j,
                # check if id_in_session is in the bots ID list
                '_is_bot': use_cli_bots or use_browser_bots,
             }
             for id_in_session, j in enumerate(start_order, start=1)])

        ParticipantLockModel.objects.bulk_create([
            ParticipantLockModel(participant_code=participant.code)
            for participant in participants])

        try:
            for app_name in session_config['app_sequence']:

                models_module = get_models_module(app_name)
                app_constants = get_app_constants(app_name)

                num_subsessions += app_constants.num_rounds
                round_numbers = list(range(1, app_constants.num_rounds + 1))

                subs = bulk_create(
                    models_module.Subsession,
                    [{'round_number': round_number}
                     for round_number in round_numbers])

                # Create players
                models_module.Player.objects.bulk_create([
                    models_module.Player(
                        session=session,
                        subsession=subsession,
                        round_number=round_number,
                        participant=participant)
                    for round_number, subsession in zip(round_numbers, subs)
                    for participant in participants])

            session._create_groups_and_initialize()

        # session.has_bots = any(p.is_bot ...)

        # handle case where DB has missing column or table
        # missing table: OperationalError: no such table: pg_subsession
        # missing column: OperationalError: table pg_player has no column
        # named contribution2
        except OperationalError as exception:
            exception_str = str(exception)
            if 'table' in exception_str:
                ExceptionClass = type(exception)
                six.reraise(
                    ExceptionClass,
                    ExceptionClass('{} - Try resetting the database.'.format(
                        exception_str)),
                    sys.exc_info()[2])
            raise

        session.build_participant_to_player_lookups()
        # automatically save all objects since the cache was activated:
        # Player, Group, Subsession, Participant, Session
        otree.db.idmap.save_objects()
        otree.db.idmap.deactivate_cache()

    if use_browser_bots:
        # what about clear_browser_bots? if session is created through
        # UI, when do we run that? it should be run when the session
        # is deleted
        try:
            num_players_total = num_participants * num_subsessions
            otree.bots.browser.initialize_bots(
                session.code, num_players_total)
        except:
            session.delete()
            raise

    session.ready = True
    session.save()

    # this should happen after session.ready = True
    if room_name is not None:
        from otree.room import ROOM_DICT
        room = ROOM_DICT[room_name]
        room.session = session

    return session


default_app_config = 'otree.session.apps.OtreeSessionConfig'
