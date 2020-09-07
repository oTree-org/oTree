import codecs
from collections import OrderedDict

import schema

from otree.models_concrete import RoomToSession
from otree.common_internal import (
    add_params_to_url, make_hash, validate_alphanumeric)
from django.conf import settings
from django.urls import reverse
from django.db import transaction

class Room(object):

    def __init__(self, name, display_name, use_secure_urls, participant_label_file=None):
        self.name = validate_alphanumeric(
            name,
            identifier_description='settings.ROOMS room name')
        if use_secure_urls and not participant_label_file:
            raise ValueError(
                'Room "{}": you must either set "participant_label_file", '
                'or set "use_secure_urls": False'.format(name)
            )
        self.participant_label_file = participant_label_file
        self.display_name = display_name
        # secure URLs are complicated, don't use them by default
        self.use_secure_urls = use_secure_urls

    def has_session(self):
        return self.get_session() is not None

    def get_session(self):
        try:
            return RoomToSession.objects.select_related('session').get(
                room_name=self.name).session
        except RoomToSession.DoesNotExist:
            return None

    def set_session(self, session):
        with transaction.atomic():
            RoomToSession.objects.filter(room_name=self.name).delete()
            if session:
                RoomToSession.objects.create(
                    room_name=self.name,
                    session=session
                )

    def has_participant_labels(self):
        return bool(self.participant_label_file)

    def get_participant_labels(self):
        '''
        Decided to just re-read the file on every request,
        rather than loading in the DB. Reasons:

        (1) Simplifies the code; we don't need an ExpectedRoomParticipant model,
            and don't need to load data into there (which involves considerations
            of race conditions)
        (2) Don't need any complicated rule deciding when to reload the file,
            whether it's upon starting the process or resetting the database,
            or both. Should the status be stored in the DB or in the process?
        (3) Checking if a given participant label is in the file is actually faster
            than looking it up in the DB table, even with .filter() and and index!
            (tested on Postgres with 10000 iterations: 17s vs 18s)
        '''

        # if i refactor this, i should use chardet instead
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
                        validate_alphanumeric(
                            label,
                            identifier_description='participant label'
                        )
                        if label not in seen:
                            labels.append(label)
                            seen.add(label)
            except UnicodeDecodeError:
                continue
            except FileNotFoundError:
                msg = (
                    'settings.ROOMS: The room "{}" references '
                    ' nonexistent participant_label_file "{}".'
                )
                raise FileNotFoundError(
                    msg.format(self.name, self.participant_label_file)
                ) from None
            else:
                return labels
        raise Exception(
            'settings.ROOMS: participant_label_file "{}" '
            'not encoded correctly.'.format(self.participant_label_file)
        )

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


def augment_room(room, ROOM_DEFAULTS):
    new_room = {}
    new_room.update(ROOM_DEFAULTS)
    new_room.update(room)
    return new_room


def get_room_dict():
    room_defaults_schema = schema.Schema(
        {
            schema.Optional('use_secure_urls', default=False): bool,
            schema.Optional('participant_label_file'): str,
        }
    )

    room_schema = schema.Schema(
        {
            'name': str,
            'display_name': str,
            schema.Optional('use_secure_urls'): bool,
            schema.Optional('participant_label_file'): str,
        }
    )

    ROOM_DICT = OrderedDict()
    ROOM_DEFAULTS = getattr(settings, 'ROOM_DEFAULTS', {})
    try:
        ROOM_DEFAULTS = room_defaults_schema.validate(ROOM_DEFAULTS)
    except schema.SchemaError as e:
        raise (ValueError('settings.ROOM_DEFAULTS: {}'.format(e))) from None
    for room in getattr(settings, 'ROOMS', []):
        room = augment_room(room, ROOM_DEFAULTS)
        try:
            room = room_schema.validate(room)
        except schema.SchemaError as e:
            raise(ValueError('settings.ROOMS: {}'.format(e))) from None
        room_object = Room(**room)
        ROOM_DICT[room_object.name] = room_object
    return ROOM_DICT

ROOM_DICT = get_room_dict()
