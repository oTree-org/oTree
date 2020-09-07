#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import django.test
from django.core.urlresolvers import reverse

from otree import constants_internal
import otree.common_internal
from otree.common_internal import random_chars_8, random_chars_10
from otree.db import models
from otree.models_concrete import ParticipantToPlayerLookup, RoomToSession
from .varsmixin import ModelWithVars


logger = logging.getLogger('otree')

client = django.test.Client()


# for now removing SaveTheChange

class Session(ModelWithVars):

    class Meta:
        app_label = "otree"
        # if i don't set this, it could be in an unpredictable order
        ordering = ['pk']

    config = models.JSONField(default=dict, null=True)  # type: dict
    vars = models.JSONField(default=dict)  # type: dict

    # label of this session instance
    label = models.CharField(
        max_length=300, null=True, blank=True,
        help_text='For internal record-keeping')

    experimenter_name = models.CharField(
        max_length=300, null=True, blank=True,
        help_text='For internal record-keeping')

    ready = models.BooleanField(default=False)

    code = models.CharField(
        default=random_chars_8,
        max_length=16,
        # set non-nullable, until we make our CharField non-nullable
        null=False,
        unique=True,
        doc="Randomly generated unique identifier for the session.")

    time_scheduled = models.DateTimeField(
        null=True, doc="The time at which the session is scheduled",
        help_text='For internal record-keeping', blank=True)

    time_started = models.DateTimeField(
        null=True,
        doc="The time at which the experimenter started the session")

    mturk_HITId = models.CharField(
        max_length=300, null=True, blank=True,
        help_text='Hit id for this session on MTurk')
    mturk_HITGroupId = models.CharField(
        max_length=300, null=True, blank=True,
        help_text='Hit id for this session on MTurk')
    mturk_qualification_type_id = models.CharField(
        max_length=300, null=True, blank=True,
        help_text='Qualification type that is '
                  'assigned to each worker taking hit')

    # since workers can drop out number of participants on server should be
    # greater than number of participants on mturk
    # value -1 indicates that this session it not intended to run on mturk
    mturk_num_participants = models.IntegerField(
        default=-1,
        help_text="Number of participants on MTurk")

    mturk_sandbox = models.BooleanField(
        default=True,
        help_text="Should this session be created in mturk sandbox?")

    archived = models.BooleanField(
        default=False,
        db_index=True,
        doc=("If set to True the session won't be visible on the "
             "main ViewList for sessions"))

    comment = models.TextField(blank=True)

    _anonymous_code = models.CharField(
        default=random_chars_10, max_length=10, null=False, db_index=True)

    _pre_create_id = models.CharField(max_length=300, db_index=True, null=True)

    use_browser_bots = models.BooleanField(default=False)

    # if the user clicks 'start bots' twice, this will prevent the bots
    # from being run twice.
    _cannot_restart_bots = models.BooleanField(default=False)
    _bots_finished = models.BooleanField(default=False)
    _bots_errored = models.BooleanField(default=False)
    _bot_case_number = models.PositiveIntegerField()

    is_demo = models.BooleanField(default=False)

    # whether SOME players are bots
    has_bots = models.BooleanField(default=False)

    def __unicode__(self):
        return self.code

    @property
    def participation_fee(self):
        '''This method is deprecated from public API,
        but still useful internally (like data export)'''
        return self.config['participation_fee']

    @property
    def real_world_currency_per_point(self):
        '''This method is deprecated from public API,
        but still useful internally (like data export)'''
        return self.config['real_world_currency_per_point']

    def is_for_mturk(self):
        return (not self.is_demo) and (self.mturk_num_participants > 0)

    def get_subsessions(self):
        lst = []
        app_sequence = self.config['app_sequence']
        for app in app_sequence:
            models_module = otree.common_internal.get_models_module(app)
            subsessions = models_module.Subsession.objects.filter(
                session=self
            ).order_by('round_number')
            lst.extend(list(subsessions))
        return lst

    def delete(self, using=None):
        for subsession in self.get_subsessions():
            subsession.delete()
        super(Session, self).delete(using)

    def get_participants(self):
        return self.participant_set.all()

    def get_human_participants(self):
        return self.participant_set.filter(_is_bot=False)

    def _create_groups_and_initialize(self):
        # group_by_arrival_time code used to be here
        for subsession in self.get_subsessions():
            subsession._create_groups()
            subsession.before_session_starts()
            subsession.save()

    def mturk_requester_url(self):
        if self.mturk_sandbox:
            requester_url = (
                "https://requestersandbox.mturk.com/mturk/manageHITs"
            )
        else:
            requester_url = "https://requester.mturk.com/mturk/manageHITs"
        return requester_url

    def mturk_worker_url(self):
        if self.mturk_sandbox:
            return (
                "https://workersandbox.mturk.com/mturk/preview?groupId={}"
            ).format(self.mturk_HITGroupId)
        return (
            "https://www.mturk.com/mturk/preview?groupId={}"
        ).format(self.mturk_HITGroupId)

    def advance_last_place_participants(self):

        # can't auto-advance bots, because that could break their
        # pre-determined logic
        # consider pros/cons of doing this
        participants = self.get_human_participants()

        # in case some participants haven't started
        unvisited_participants = []
        for p in participants:
            if p._index_in_pages == 0:
                unvisited_participants.append(p)
                client.get(p._start_url(), follow=True)

        if unvisited_participants:
            # that's it -- just visit the start URL, advancing by 1
            return

        last_place_page_index = min([p._index_in_pages for p in participants])
        last_place_participants = [
            p for p in participants
            if p._index_in_pages == last_place_page_index
        ]

        for p in last_place_participants:
            # what if first page is wait page?
            # that shouldn't happen, because then they must be
            # waiting for some other players who are even further back
            assert p._current_form_page_url
            try:
                resp = client.post(
                    p._current_form_page_url,
                    data={constants_internal.auto_submit: True}, follow=True
                )
            except:
                logging.exception("Failed to advance participants.")
                raise

            assert resp.status_code < 400

    def build_participant_to_player_lookups(self):
        subsession_app_names = self.config['app_sequence']

        views_modules = {}
        for app_name in subsession_app_names:
            views_modules[app_name] = (
                otree.common_internal.get_views_module(app_name))

        def views_module_for_player(player):
            return views_modules[player._meta.app_config.name]

        records_to_create = []

        for participant in self.get_participants():
            page_index = 0
            for player in participant.get_players():
                for View in views_module_for_player(player).page_sequence:
                    page_index += 1
                    records_to_create.append(
                        ParticipantToPlayerLookup(
                            participant=participant,
                            page_index=page_index,
                            app_name=player._meta.app_config.name,
                            player_pk=player.pk,
                            url=reverse(View.url_name(),
                                        args=[participant.code, page_index]))
                    )

            # technically could be stored at the session level
            participant._max_page_index = page_index
            participant.save()
        ParticipantToPlayerLookup.objects.bulk_create(records_to_create)

    def get_room(self):
        from otree.room import ROOM_DICT
        try:
            room_name = RoomToSession.objects.get(session=self).room_name
            return ROOM_DICT[room_name]
        except RoomToSession.DoesNotExist:
            return None
