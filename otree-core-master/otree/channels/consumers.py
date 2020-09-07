#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import django.db
import django.utils.timezone
from datetime import timedelta

from channels import Group

import otree.session
from otree.models import Participant, Session
from otree.models_concrete import (
    CompletedGroupWaitPage, CompletedSubsessionWaitPage)
from otree.common_internal import (
    channels_wait_page_group_name, channels_create_session_group_name)
from otree.models_concrete import (
    FailedSessionCreation, ParticipantRoomVisit,
    FAILURE_MESSAGE_MAX_LENGTH, BrowserBotsLauncherSessionCode)
from otree.room import ROOM_DICT


def connect_wait_page(message, params):
    session_pk, page_index, model_name, model_pk = params.split(',')
    session_pk = int(session_pk)
    page_index = int(page_index)
    model_pk = int(model_pk)

    group_name = channels_wait_page_group_name(
        session_pk, page_index, model_name, model_pk
    )
    group = Group(group_name)
    group.add(message.reply_channel)

    # in case message was sent before this web socket connects
    if model_name == 'group':
        ready = CompletedGroupWaitPage.objects.filter(
            page_index=page_index,
            group_pk=model_pk,
            session_id=session_pk,
            after_all_players_arrive_run=True).exists()
    else:  # subsession
        ready = CompletedSubsessionWaitPage.objects.filter(
            page_index=page_index,
            session_id=session_pk,
            after_all_players_arrive_run=True).exists()
    if ready:
        message.reply_channel.send(
            {'text': json.dumps(
                {'status': 'ready'})})


def disconnect_wait_page(message, params):
    session_pk, page_index, model_name, model_pk = params.split(',')
    page_index = int(page_index)
    model_pk = int(model_pk)

    group_name = channels_wait_page_group_name(
        session_pk, page_index, model_name, model_pk
    )
    group = Group(group_name)
    group.discard(message.reply_channel)


def connect_auto_advance(message, params):
    participant_code, page_index = params.split(',')
    page_index = int(page_index)

    group = Group('auto-advance-{}'.format(participant_code))
    group.add(message.reply_channel)

    # in case message was sent before this web socket connects

    try:
        participant = Participant.objects.get(code=participant_code)
    except Participant.DoesNotExist:
        message.reply_channel.send(
            {'text': json.dumps(
                # doesn't get shown because not yet localized
                {'error': 'Participant not found in database.'})})
        return
    if participant._index_in_pages > page_index:
        message.reply_channel.send(
            {'text': json.dumps(
                {'new_index_in_pages': participant._index_in_pages})})


def disconnect_auto_advance(message, params):
    participant_code, page_index = params.split(',')

    group = Group('auto-advance-{}'.format(participant_code))
    group.discard(message.reply_channel)


def create_session(message):
    group = Group(message['channels_group_name'])

    kwargs = message['kwargs']

    # because it's launched through web UI
    kwargs['honor_browser_bots_config'] = True
    try:
        otree.session.create_session(**kwargs)
    except Exception as e:
        # full error message is printed to console (though sometimes not?)
        error_message = (
            'Failed to create session: "{}" - '
            'For the full traceback, check the server logs.'.format(
                    str(e)))
        group.send(
            {'text': json.dumps(
                {'error': error_message})}
        )
        FailedSessionCreation.objects.create(
            pre_create_id=kwargs['_pre_create_id'],
            message=error_message[:FAILURE_MESSAGE_MAX_LENGTH]
        )
        raise

    group.send(
        {'text': json.dumps(
            {'status': 'ready'})}
    )

    if 'room_name' in kwargs:
        Group('room-participants-{}'.format(kwargs['room_name'])).send(
            {'text': json.dumps(
                {'status': 'session_ready'})}
        )


def connect_wait_for_session(message, pre_create_id):
    group = Group(channels_create_session_group_name(pre_create_id))
    group.add(message.reply_channel)

    # in case message was sent before this web socket connects
    if Session.objects.filter(_pre_create_id=pre_create_id, ready=True):
        group.send(
            {'text': json.dumps(
                {'status': 'ready'})}
        )
    else:
        failures = FailedSessionCreation.objects.filter(
            pre_create_id=pre_create_id
        )
        if failures:
            failure = failures[0]
            group.send(
                {'text': json.dumps(
                    {'error': failure.message})}
            )


def disconnect_wait_for_session(message, pre_create_id):
    group = Group(
        channels_create_session_group_name(pre_create_id)
    )
    group.discard(message.reply_channel)


def connect_room_admin(message, room):
    Group('room-admin-{}'.format(room)).add(message.reply_channel)

    room_object = ROOM_DICT[room]

    now = django.utils.timezone.now()
    stale_threshold = now - timedelta(seconds=15)
    present_list = ParticipantRoomVisit.objects.filter(
        room_name=room_object.name,
        last_updated__gte=stale_threshold,
    ).values_list('participant_label', flat=True)

    # make it JSON serializable
    present_list = list(present_list)

    message.reply_channel.send({'text': json.dumps({
        'status': 'load_participant_lists',
        'participants_present': present_list,
    })})

    # prune very old visits -- don't want a resource leak
    # because sometimes not getting deleted on WebSocket disconnect
    very_stale_threshold = now - timedelta(minutes=10)
    ParticipantRoomVisit.objects.filter(
        room_name=room_object.name,
        last_updated__lt=very_stale_threshold,
    ).delete()


def disconnect_room_admin(message, room):
    Group('room-admin-{}'.format(room)).discard(message.reply_channel)


def connect_room_participant(message, params):
    room_name, participant_label, tab_unique_id = params.split(',')
    room = ROOM_DICT[room_name]

    Group('room-participants-{}'.format(room_name)).add(message.reply_channel)

    if room.has_session():
        message.reply_channel.send(
            {'text': json.dumps({'status': 'session_ready'})}
        )
    else:
        try:
            ParticipantRoomVisit.objects.create(
                participant_label=participant_label,
                room_name=room_name,
                tab_unique_id=tab_unique_id
            )
        except django.db.IntegrityError:
            # possible that the tab connected twice
            # without disconnecting in between
            # because of WebSocket failure
            # tab_unique_id is unique=True,
            # so this will throw an integrity error.
            pass
        Group('room-admin-{}'.format(room_name)).send({'text': json.dumps({
            'status': 'add_participant',
            'participant': participant_label
        })})


def disconnect_room_participant(message, params):
    room_name, participant_label, tab_unique_id = params.split(',')
    room = ROOM_DICT[room_name]

    Group('room-participants-{}'.format(room_name)).discard(
        message.reply_channel)

    # should use filter instead of get,
    # because if the DB is recreated,
    # the record could already be deleted
    ParticipantRoomVisit.objects.filter(
        participant_label=participant_label,
        room_name=room_name,
        tab_unique_id=tab_unique_id).delete()

    if room.has_participant_labels():
        if not ParticipantRoomVisit.objects.filter(
            participant_label=participant_label,
            room_name=room_name
        ).exists():
            # it's ok if there is a race condition --
            # in JS removing a participant is idempotent
            Group('room-admin-{}'.format(room_name)).send({'text': json.dumps({
                'status': 'remove_participant',
                'participant': participant_label
            })})
    else:
        Group('room-admin-{}'.format(room_name)).send({'text': json.dumps({
            'status': 'remove_participant',
        })})


def connect_browser_bots_client(message, session_code):
    Group('browser-bots-client-{}'.format(session_code)).add(
        message.reply_channel)


def disconnect_browser_bots_client(message, session_code):
    Group('browser-bots-client-{}'.format(session_code)).discard(
        message.reply_channel)


def connect_browser_bot(message):

    Group('browser_bot_wait').add(message.reply_channel)
    launcher_session_info = BrowserBotsLauncherSessionCode.objects.first()
    if launcher_session_info:
        message.reply_channel.send(
            {'text': json.dumps({'status': 'session_ready'})}
        )


def disconnect_browser_bot(message):
    Group('browser_bot_wait').discard(message.reply_channel)


def connect_session_admin(message, session_code):
    Group('session-admin-{}'.format(session_code)).add(
        message.reply_channel)
    Session.objects.get(code=session_code)
    # don't do the redundant check because it could be bothersome


def disconnect_session_admin(message, session_code):
    Group('session-admin-{}'.format(session_code)).discard(
        message.reply_channel)
