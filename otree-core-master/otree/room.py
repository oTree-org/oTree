#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import errno
from collections import OrderedDict

import schema

from otree.models_concrete import RoomToSession, ExpectedRoomParticipant
from otree.common_internal import (
    add_params_to_url, make_hash, validate_identifier)
from otree.views.abstract import global_lock


from django.conf import settings
from django.core.urlresolvers import reverse


class Room(object):

    def __init__(self, config_dict):
        self.participant_label_file = config_dict.get('participant_label_file')

        self.name = validate_identifier(
            config_dict['name'],
            identifier_description='settings.ROOMS room name')
        self.display_name = config_dict['display_name']
        # secure URLs are complicated, don't use them by default
        self.use_secure_urls = config_dict['use_secure_urls']
        self.pin_code = config_dict.get('pin_code')
        self._participant_labels_loaded = False
        if self.use_secure_urls and not self.participant_label_file:
            raise ValueError(
                'Room "{}": you must either set "participant_label_file", '
                'or set "use_secure_urls": False'.format(self.name)
            )

    def has_session(self):
        return self.session is not None

    @property
    def session(self):
        try:
            return RoomToSession.objects.select_related('session').get(
                room_name=self.name).session
        except RoomToSession.DoesNotExist:
            return None

    @session.setter
    def session(self, session):
        RoomToSession.objects.filter(room_name=self.name).delete()
        if session:
            RoomToSession.objects.create(
                room_name=self.name,
                session=session
            )

    def has_participant_labels(self):
        return bool(self.participant_label_file)

    def load_participant_labels_to_db(self):
        if self.has_participant_labels():
            encodings = ['ascii', 'utf-8', 'utf-16']
            for e in encodings:
                try:
                    plabel_path = self.participant_label_file
                    with codecs.open(plabel_path, "r", encoding=e) as f:
                        seen = set()
                        labels = []
                        for line in f:
                            label = line.strip()
                            if not label:
                                continue
                            label = validate_identifier(
                                line.strip(),
                                identifier_description='participant label'
                            )
                            if label not in seen:
                                labels.append(label)
                                seen.add(label)
                except UnicodeDecodeError:
                    continue
                except OSError as err:
                    # this code is equivalent to "except FileNotFoundError:"
                    # but works in py2 and py3
                    if err.errno == errno.ENOENT:
                        msg = (
                            'settings.ROOMS: The room "{}" references '
                            ' nonexistent participant_label_file "{}".'
                        )
                        raise IOError(
                            msg.format(self.name, self.participant_label_file))
                    raise err
                else:
                    with global_lock():
                        # before I used select_for_update to prevent race
                        # conditions. But the queryset was not evaluated
                        # so it did not hit the DB. maybe simpler to use an
                        # explicit lock
                        ExpectedRoomParticipant.objects.select_for_update()
                        ExpectedRoomParticipant.objects.filter(
                            room_name=self.name).delete()
                        ExpectedRoomParticipant.objects.bulk_create(
                            ExpectedRoomParticipant(
                                room_name=self.name,
                                participant_label=participant_label
                            ) for participant_label in labels
                        )
                    self._participant_labels_loaded = True
                    return
            raise Exception(
                'settings.ROOMS: participant_label_file "{}" '
                'not encoded correctly.'.format(self.participant_label_file)
            )
        raise Exception('no guestlist')

    def get_participant_labels(self):
        if self.has_participant_labels():
            if not self._participant_labels_loaded:
                self.load_participant_labels_to_db()
            return ExpectedRoomParticipant.objects.filter(
                    room_name=self.name
                ).order_by('id').values_list('participant_label', flat=True)
        raise Exception('no guestlist')

    def num_participant_labels(self):
        if not self._participant_labels_loaded:
            self.load_participant_labels_to_db()
        return ExpectedRoomParticipant.objects.filter(
            room_name=self.name
        ).count()

    def get_room_wide_url(self, request):
        url = reverse('AssignVisitorToRoom', args=(self.name,))
        return request.build_absolute_uri(url)

    def get_participant_urls(self, request):
        participant_urls = []
        room_base_url = reverse('AssignVisitorToRoom', args=(self.name,))
        room_base_url = request.build_absolute_uri(room_base_url)

        if self.has_participant_labels():
            for label in self.get_participant_labels():
                params = {'participant_label': label}
                if self.use_secure_urls:
                    params['hash'] = make_hash(label)
                participant_url = add_params_to_url(room_base_url, params)
                participant_urls.append(participant_url)

        return participant_urls

    def has_pin_code(self):
        return bool(self.pin_code)

    def get_pin_code(self):
        return self.pin_code


def augment_room(room, ROOM_DEFAULTS):
    new_room = {'doc': ''}
    new_room.update(ROOM_DEFAULTS)
    new_room.update(room)
    return new_room


def get_room_dict():
    room_defaults_schema = schema.Schema(
        {
            schema.Optional('use_secure_urls', default=False): bool,
            schema.Optional('participant_label_file'): str,
            schema.Optional('doc'): str,
        }
    )

    room_schema = schema.Schema(
        {
            'name': str,
            'display_name': str,
            schema.Optional('use_secure_urls'): bool,
            schema.Optional('participant_label_file'): str,
            schema.Optional('doc'): str,
        }
    )

    ROOM_DICT = OrderedDict()
    ROOM_DEFAULTS = getattr(settings, 'ROOM_DEFAULTS', {})
    try:
        ROOM_DEFAULTS = room_defaults_schema.validate(ROOM_DEFAULTS)
    except schema.SchemaError as e:
        raise (ValueError('settings.ROOM_DEFAULTS: {}'.format(e)))
    for room in getattr(settings, 'ROOMS', []):
        room = augment_room(room, ROOM_DEFAULTS)
        try:
            room = room_schema.validate(room)
        except schema.SchemaError as e:
            raise(ValueError('settings.ROOMS: {}'.format(e)))
        room_object = Room(room)
        ROOM_DICT[room_object.name] = room_object
    return ROOM_DICT

ROOM_DICT = get_room_dict()
