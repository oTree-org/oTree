#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import sys
from functools import reduce
from collections import OrderedDict
from decimal import Decimal
import warnings
from django.urls import reverse
from django.conf import settings
from django.db import transaction
from django.db.utils import OperationalError

import otree.db.idmap
from otree.models import Participant, Session
from otree.common_internal import (
    get_models_module, get_app_constants, validate_alphanumeric,
    get_bots_module)
from otree import common_internal
import otree.common_internal
from otree.common import RealWorldCurrency
from otree.models_concrete import ParticipantLockModel, ParticipantToPlayerLookup
import otree.bots.browser
from collections import defaultdict


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


class SessionConfigError(Exception):
    pass


class SessionConfig(dict):

    # convenient access
    @property
    def app_sequence(self) -> list:
        return self['app_sequence']

    @property
    def participation_fee(self) -> RealWorldCurrency:
        return self['participation_fee']

    def get_lcm(self):
        min_multiple_list = []
        for app_name in self['app_sequence']:
            Constants = get_app_constants(app_name)
            # if players_per_group is None, 0, etc.
            min_multiple = Constants.players_per_group or 1
            min_multiple_list.append(min_multiple)
        return lcmm(*min_multiple_list)

    def get_num_bot_cases(self):
        num_cases = 1
        for app_name in self['app_sequence']:
            bots_module = get_bots_module(app_name)
            cases = bots_module.PlayerBot.cases
            num_cases = max(num_cases, len(cases))
        return num_cases

    def clean(self):

        required_keys = [
            'name',
            'app_sequence',
            'num_demo_participants',
            'participation_fee',
            'real_world_currency_per_point',
        ]

        for key in required_keys:
            if key not in self:
                raise SessionConfigError(
                    'settings.SESSION_CONFIGS: all configs must have a '
                    '"{}"'.format(key)
                )

        datatypes = {
            'app_sequence': list,
            'num_demo_participants': int,
            'name': str,
        }

        for key, datatype in datatypes.items():
            if not isinstance(self[key], datatype):
                msg = (
                    'SESSION_CONFIGS "{}": '
                    'the entry "{}" must be of type {}'
                ).format(self['name'], key, datatype.__name__)
                raise SessionConfigError(msg)

        # Allow non-ASCII chars in session config keys, because they are
        # configurable in the admin, so need to be readable by non-English
        # speakers. However, don't allow punctuation, spaces, etc.
        # They make it harder to reason about and could cause problems
        # later on. also could uglify the user's code.

        INVALID_IDENTIFIER_MSG = (
            'Key "{}" in settings.SESSION_CONFIGS '
            'must not contain spaces, punctuation, '
            'or other special characters. '
            'It can contain non-English characters, '
            'but it must be a valid Python variable name '
            'according to string.isidentifier().'
        )

        for key in self:
            if not key.isidentifier():
                raise SessionConfigError(INVALID_IDENTIFIER_MSG.format(key))

        validate_alphanumeric(
            self['name'],
            identifier_description='settings.SESSION_CONFIGS name'
        )

        app_sequence = self['app_sequence']
        if len(app_sequence) != len(set(app_sequence)):
            msg = (
                'settings.SESSION_CONFIGS: '
                'app_sequence of "{}" '
                'must not contain duplicate elements. '
                'If you want multiple rounds, '
                'you should set Constants.num_rounds.')
            raise SessionConfigError(msg.format(self['name']))

        if len(app_sequence) == 0:
            raise SessionConfigError(
                'settings.SESSION_CONFIGS: app_sequence cannot be empty.')

        self.setdefault('display_name', self['name'])
        self.setdefault('doc', '')

        self['participation_fee'] = RealWorldCurrency(
            self['participation_fee'])

    def app_sequence_display(self):
        app_sequence = []
        for app_name in self['app_sequence']:
            models_module = get_models_module(app_name)
            num_rounds = models_module.Constants.num_rounds
            if num_rounds > 1:
                formatted_app_name = '{} ({} rounds)'.format(
                    app_name, num_rounds)
            else:
                formatted_app_name = app_name
            subsssn = {
                'doc': getattr(models_module, 'doc', ''),
                'name': formatted_app_name}
            app_sequence.append(subsssn)
        return app_sequence

    non_editable_fields = {
        'app_sequence',
        'name',
        'display_name',
        'app_sequence',
        'num_demo_participants',
        'doc',
        'num_bots',
    }

    def builtin_editable_fields(self):
        fields = ['participation_fee']
        if settings.USE_POINTS:
            fields.append('real_world_currency_per_point')
        return fields

    def custom_editable_fields(self):
        # should there also be some restriction on
        # what chars are allowed? because maybe not all chars work
        # in an HTML form field (e.g. periods, quotes, etc)
        # so far, it seems any char works OK, even without escaping
        # before making an HTML attribute. even '>漢 ."&'
        # so i'll just put a general recommendation in the docs

        return [
            k for k, v in self.items()
            if k not in self.non_editable_fields
            and k not in self.builtin_editable_fields()
            and type(v) in [bool, int, float, str]]

    def editable_fields(self):
        return self.builtin_editable_fields() + self.custom_editable_fields()

    def html_field_name(self, field_name):
        return '{}.{}'.format(self['name'], field_name)

    def editable_field_html(self, field_name):
        existing_value = self[field_name]
        html_field_name = self.html_field_name(field_name)
        base_attrs = ["name='{}'".format(html_field_name)]

        if isinstance(existing_value, bool):
            attrs = [
                "type='checkbox'",
                'checked' if existing_value else '',
                # don't use class=form-control because it looks too big,
                # like it's intended for mobile devices
            ]
        elif isinstance(existing_value, int):
            attrs = [
                "type='number'",
                "required",
                "step='1'",
                "value='{}'".format(existing_value),
                "class='form-control'",
            ]
        elif isinstance(existing_value, (float, Decimal)):
            # convert to float, e.g. participation_fee
            attrs = [
                "class='form-control'",
                "type='number'",
                "step='any'",
                "required",
                "value='{}'".format(float(existing_value)),
            ]
        elif isinstance(existing_value, str):
            attrs = [
                "type='text'",
                "value='{}'".format(existing_value),
                "class='form-control'"
            ]
        html = '''
        <tr><td><b>{}</b><td><input {}></td>
        '''.format(field_name, ' '.join(base_attrs + attrs))
        return html

    def builtin_editable_fields_html(self):
        return [self.editable_field_html(k)
                for k in self.builtin_editable_fields()]

    def custom_editable_fields_html(self):
        return [self.editable_field_html(k)
                for k in self.custom_editable_fields()]


def get_session_configs_dict():
    SESSION_CONFIGS_DICT = OrderedDict()
    for config_dict in settings.SESSION_CONFIGS:
        config_obj = SessionConfig(settings.SESSION_CONFIG_DEFAULTS)
        config_obj.update(config_dict)
        config_obj.clean()
        SESSION_CONFIGS_DICT[config_dict['name']] = config_obj
    return SESSION_CONFIGS_DICT

SESSION_CONFIGS_DICT = get_session_configs_dict()


def create_session(
        session_config_name, *, num_participants, label='',
        room_name=None, is_mturk=False,
        is_demo=False,
        edited_session_config_fields=None) -> Session:

    num_subsessions = 0
    edited_session_config_fields = edited_session_config_fields or {}

    try:
        session_config = SESSION_CONFIGS_DICT[session_config_name]
    except KeyError:
        msg = 'Session config "{}" not found in settings.SESSION_CONFIGS.'
        raise KeyError(msg.format(session_config_name)) from None
    else:
        # copy so that we don't mutate the original
        # .copy() returns a dict, so need to convert back to SessionConfig
        session_config = SessionConfig(session_config.copy())
        session_config.update(edited_session_config_fields)

        # check validity and converts serialized decimal & currency values
        # back to their original data type (because they were serialized
        # when passed through channels
        session_config.clean()

    with transaction.atomic():
        # 2014-5-2: i could implement this by overriding the __init__ on the
        # Session model, but I don't really know how that works, and it seems
        # to be a bit discouraged: http://goo.gl/dEXZpv
        # 2014-9-22: preassign to groups for demo mode.

        if is_mturk:
            mturk_num_participants = (
                    num_participants /
                    settings.MTURK_NUM_PARTICIPANTS_MULTIPLE)
        else:
            mturk_num_participants = -1

        session = Session.objects.create(
            config=session_config,
            label=label,
            is_demo=is_demo,
            num_participants=num_participants,
            mturk_num_participants=mturk_num_participants
            ) # type: Session

        # check that it divides evenly
        session_lcm = session_config.get_lcm()
        if num_participants % session_lcm:
            msg = (
                'Session Config {}: Number of participants ({}) is not a multiple '
                'of group size ({})'
            ).format(session_config['name'], num_participants, session_lcm)
            raise ValueError(msg)

        Participant.objects.bulk_create(
            [
                Participant(id_in_session=id_in_session, session=session)
                for id_in_session in list(range(1, num_participants+1))
            ]
        )

        participant_values = session.participant_set.order_by('id').values('code', 'id')

        ParticipantLockModel.objects.bulk_create([
            ParticipantLockModel(participant_code=participant['code'])
            for participant in participant_values])

        participant_to_player_lookups = []
        page_index = 0

        for app_name in session_config['app_sequence']:

            views_module = common_internal.get_pages_module(app_name)
            models_module = get_models_module(app_name)
            Constants = models_module.Constants
            num_subsessions += Constants.num_rounds

            round_numbers = list(range(1, Constants.num_rounds + 1))

            Subsession = models_module.Subsession
            Group = models_module.Group
            Player = models_module.Player

            Subsession.objects.bulk_create(
                [
                    Subsession(round_number=round_number, session=session)
                    for round_number in round_numbers
                ]
            )

            subsessions = Subsession.objects.filter(
                session=session).order_by('round_number').values(
                'id', 'round_number')

            ppg = Constants.players_per_group
            if ppg is None or Subsession._has_group_by_arrival_time():
                ppg = num_participants

            num_groups_per_round = int(num_participants/ppg)

            groups_to_create = []
            for subsession in subsessions:
                for id_in_subsession in range(1, num_groups_per_round+1):
                    groups_to_create.append(
                        Group(
                            session=session,
                            subsession_id=subsession['id'],
                            round_number=subsession['round_number'],
                            id_in_subsession=id_in_subsession,
                        )
                    )

            Group.objects.bulk_create(groups_to_create)

            groups = Group.objects.filter(session=session).values(
                'id_in_subsession', 'subsession_id', 'id'
            ).order_by('id_in_subsession')

            groups_lookup = defaultdict(list)

            for group in groups:
                subsession_id = group['subsession_id']
                groups_lookup[subsession_id].append(group['id'])

            players_to_create = []

            for subsession in subsessions:
                subsession_id=subsession['id']
                round_number=subsession['round_number']
                participant_index = 0
                for group_id in groups_lookup[subsession_id]:
                    for id_in_group in range(1, ppg+1):
                        participant = participant_values[participant_index]
                        players_to_create.append(
                            Player(
                                session=session,
                                subsession_id=subsession_id,
                                round_number=round_number,
                                participant_id=participant['id'],
                                group_id=group_id,
                                id_in_group=id_in_group
                            )
                        )
                        participant_index += 1

            # Create players
            Player.objects.bulk_create(players_to_create)

            players_flat = Player.objects.filter(session=session).values(
                'id', 'participant__code', 'participant__id', 'subsession__id',
                'round_number'
            )

            players_by_round = [[] for _ in range(Constants.num_rounds)]
            for p in players_flat:
                players_by_round[p['round_number']-1].append(p)

            for round_number, round_players in enumerate(players_by_round, start=1):
                for View in views_module.page_sequence:
                    page_index += 1
                    for p in round_players:

                        participant_code = p['participant__code']

                        url = View.get_url(
                            participant_code=participant_code,
                            name_in_url=Constants.name_in_url,
                            page_index=page_index
                        )

                        participant_to_player_lookups.append(
                            ParticipantToPlayerLookup(
                                participant_id=p['participant__id'],
                                participant_code=participant_code,
                                page_index=page_index,
                                app_name=app_name,
                                player_pk=p['id'],
                                subsession_pk=p['subsession__id'],
                                session_pk=session.pk,
                                url=url))

        ParticipantToPlayerLookup.objects.bulk_create(
            participant_to_player_lookups
        )
        session.participant_set.update(_max_page_index=page_index)

        with otree.db.idmap.use_cache():
            # possible optimization: check if
            # Subsession.creating_session == BaseSubsession.creating_session
            # if so, skip it.
            # but this will only help people who didn't override creating_session
            # in that case, the session usually creates quickly, anyway.
            for subsession in session.get_subsessions():
                subsession.before_session_starts()
                subsession.creating_session()
            otree.db.idmap.save_objects()

        # 2017-09-27: moving this inside the transaction
        session._set_admin_report_app_names()
        session.save()
        # we don't need to mark it ready=True here...because it's in a
        # transaction

    # this should happen after session.ready = True
    if room_name is not None:
        from otree.room import ROOM_DICT
        room = ROOM_DICT[room_name]
        room.set_session(session)

    return session


default_app_config = 'otree.session.apps.OtreeSessionConfig'
