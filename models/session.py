#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import channels
import json
from django.urls import reverse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from otree.channels.utils import auto_advance_group

from otree import constants_internal
import otree.common_internal
from otree.common_internal import (
    random_chars_8, random_chars_10, get_admin_secret_code,
    get_app_label_from_name
)
import time

from otree.db import models
from otree.models_concrete import ParticipantToPlayerLookup, RoomToSession
from django.template.loader import select_template
from django.template import TemplateDoesNotExist
from .varsmixin import ModelWithVars


logger = logging.getLogger('otree')


ADMIN_SECRET_CODE = get_admin_secret_code()

import model_utils

class Session(ModelWithVars):
    _ft = model_utils.FieldTracker()

    class Meta:
        app_label = "otree"
        # if i don't set this, it could be in an unpredictable order
        ordering = ['pk']

    _pickle_fields = ['vars', 'config']
    config = models._PickleField(default=dict, null=True)  # type: dict

    # label of this session instance
    label = models.CharField(
        max_length=300, null=True, blank=True,
        help_text='For internal record-keeping')

    experimenter_name = models.CharField(
        max_length=300, null=True, blank=True,
        help_text='For internal record-keeping')

    code = models.CharField(
        default=random_chars_8,
        max_length=16,
        # set non-nullable, until we make our CharField non-nullable
        null=False,
        unique=True,
        doc="Randomly generated unique identifier for the session.")

    mturk_HITId = models.CharField(
        max_length=300, null=True, blank=True,
        help_text='Hit id for this session on MTurk')
    mturk_HITGroupId = models.CharField(
        max_length=300, null=True, blank=True,
        help_text='Hit id for this session on MTurk')

    # since workers can drop out number of participants on server should be
    # greater than number of participants on mturk
    # value -1 indicates that this session it not intended to run on mturk
    mturk_num_participants = models.IntegerField(
        default=-1,
        help_text="Number of participants on MTurk")

    mturk_use_sandbox = models.BooleanField(
        default=True,
        help_text="Should this session be created in mturk sandbox?")

    # use Float instead of DateTime because DateTime
    # is a pain to work with (e.g. naive vs aware datetime objects)
    # and there is no need here for DateTime
    mturk_expiration = models.FloatField(
        null=True
    )

    archived = models.BooleanField(
        default=False,
        db_index=True,
        doc=("If set to True the session won't be visible on the "
             "main ViewList for sessions"))

    comment = models.TextField(blank=True)

    _anonymous_code = models.CharField(
        default=random_chars_10, max_length=10, null=False, db_index=True)

    def use_browser_bots(self):
        return self.participant_set.filter(is_browser_bot=True).exists()

    is_demo = models.BooleanField(default=False)

    _admin_report_app_names = models.TextField(default='')
    _admin_report_num_rounds = models.CharField(default='', max_length=255)

    num_participants = models.PositiveIntegerField()

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

    def is_mturk(self):
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

    def get_participants(self):
        return list(self.participant_set.order_by('id_in_session'))

    def mturk_worker_url(self):
        # different HITs
        # get the same preview page, because they are lumped into the same
        # "hit group". This is not documented, but it seems HITs are lumped
        # if a certain subset of properties are the same:
        # https://forums.aws.amazon.com/message.jspa?messageID=597622#597622
        # this seems like the correct design; the only case where this will
        # not work is if the HIT was deleted from the server, but in that case,
        # the HIT itself should be canceled.


        # 2018-06-04:
        # the format seems to have changed to this:
        # https://worker.mturk.com/projects/{group_id}/tasks?ref=w_pl_prvw
        # but the old format still works.
        # it seems I can't replace groupId by hitID, which i would like to do
        # because it's more precise.
        subdomain = "workersandbox" if self.mturk_use_sandbox else 'www'
        return "https://{}.mturk.com/mturk/preview?groupId={}".format(
            subdomain,
            self.mturk_HITGroupId
        )

    def mturk_is_expired(self):
        # self.mturk_expiration is offset-aware, so therefore we must compare
        # it against an offset-aware value.
        return self.mturk_expiration and self.mturk_expiration < time.time()

    def mturk_is_active(self):
        return self.mturk_HITId and not self.mturk_is_expired()

    def advance_last_place_participants(self):
        # django.test takes 0.5 sec to import,
        # if this is done globally then it adds to each startup
        # it's only used here, and often isn't used at all.
        # so best to do it only here
        # it gets cached
        import django.test
        client = django.test.Client()

        participants = self.get_participants()

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
            try:
                current_form_page_url = p._current_form_page_url
                if current_form_page_url:
                    resp = client.post(
                        current_form_page_url,
                        data={
                            constants_internal.timeout_happened: True,
                            constants_internal.admin_secret_code: ADMIN_SECRET_CODE
                        },
                        follow=True
                    )
                    # not sure why, but many users are getting HttpResponseNotFound
                    if resp.status_code >= 400:
                        msg = ('Submitting page {} failed, '
                            'returned HTTP status code {}.'.format(
                                current_form_page_url, resp.status_code
                            ))
                        content = resp.content
                        if len(content) < 600:
                            msg += ' response content: {}'.format(content)
                        raise AssertionError(msg)

                else:
                    # it's possible that the slowest user is on a wait page,
                    # especially if their browser is closed.
                    # because they were waiting for another user who then
                    # advanced past the wait page, but they were never
                    # advanced themselves.
                    start_url = p._start_url()
                    resp = client.get(start_url, follow=True)
            except:
                logging.exception("Failed to advance participants.")
                raise

            # do the auto-advancing here,
            # rather than in increment_index_in_pages,
            # because it's only needed here.
            otree.channels.utils.sync_group_send_wrapper(
                type='auto_advanced',
                group=auto_advance_group(p.code),
                event={}
            )


    def get_room(self):
        from otree.room import ROOM_DICT
        try:
            room_name = RoomToSession.objects.get(session=self).room_name
            return ROOM_DICT[room_name]
        except RoomToSession.DoesNotExist:
            return None

    def _get_payoff_plus_participation_fee(self, payoff):
        '''For a participant who has the given payoff,
        return their payoff_plus_participation_fee
        Useful to define it here, for data export
        '''

        return (
            self.config['participation_fee'] +
            payoff.to_real_world_currency(self)
        )

    def _set_admin_report_app_names(self):

        admin_report_app_names = []
        num_rounds_list = []
        for app_name in self.config['app_sequence']:
            models_module = otree.common_internal.get_models_module(app_name)
            app_label = get_app_label_from_name(app_name)
            try:
                select_template([
                    f'{app_label}/admin_report.html',
                    f'{app_label}/AdminReport.html',
                ])
            except TemplateDoesNotExist:
                pass
            else:
                admin_report_app_names.append(app_name)
                num_rounds_list.append(models_module.Constants.num_rounds)

        self._admin_report_app_names = ';'.join(admin_report_app_names)
        self._admin_report_num_rounds = ';'.join(str(n) for n in num_rounds_list)

    def _admin_report_apps(self):
        return self._admin_report_app_names.split(';')

    def _admin_report_num_rounds_list(self):
        return [int(num) for num in self._admin_report_num_rounds.split(';')]

    def has_admin_report(self):
        return bool(self._admin_report_app_names)
