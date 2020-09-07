#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models import permalink
from django.core.urlresolvers import reverse

import otree.common_internal
from otree import constants_internal
from otree.common_internal import id_label_name, random_chars_8
from otree.common import Currency as c
from otree.db import models
from otree.models_concrete import ParticipantToPlayerLookup
from otree.models.varsmixin import ModelWithVars


class Participant(ModelWithVars):

    class Meta:
        ordering = ['pk']
        app_label = "otree"
        index_together = ['session', 'mturk_worker_id', 'mturk_assignment_id']

    session = models.ForeignKey('otree.Session')

    vars = models.JSONField(default=dict)

    label = models.CharField(
        max_length=50, null=True, doc=(
            "Label assigned by the experimenter. Can be assigned by passing a "
            "GET param called 'participant_label' to the participant's start "
            "URL"
        )
    )

    id_in_session = models.PositiveIntegerField(null=True)

    exclude_from_data_analysis = models.BooleanField(
        default=False, doc=(
            "if set to 1, the experimenter indicated that this participant's "
            "data points should be excluded from the data analysis (e.g. a "
            "problem took place during the experiment)")
    )

    time_started = models.DateTimeField(null=True)
    user_type_in_url = constants_internal.user_type_participant
    mturk_assignment_id = models.CharField(
        max_length=50, null=True)
    mturk_worker_id = models.CharField(max_length=50, null=True)

    start_order = models.PositiveIntegerField(db_index=True)

    _index_in_subsessions = models.PositiveIntegerField(default=0, null=True)

    _index_in_pages = models.PositiveIntegerField(default=0, db_index=True)

    def _id_in_session(self):
        """the human-readable version."""
        if self._is_bot:
            return 'P{} (bot)'.format(self.id_in_session)
        else:
            return 'P{}'.format(self.id_in_session)

    _waiting_for_ids = models.CharField(null=True, max_length=300)

    code = models.CharField(
        default=random_chars_8,
        max_length=16,
        # set non-nullable, until we make our CharField non-nullable
        null=False,
        # unique implies DB index
        unique=True,
        doc=(
            "Randomly generated unique identifier for the participant. If you "
            "would like to merge this dataset with those from another "
            "subsession in the same session, you should join on this field, "
            "which will be the same across subsessions."
        )
    )

    last_request_succeeded = models.BooleanField(
        verbose_name='Health of last server request'
    )

    visited = models.BooleanField(
        default=False, db_index=True,
        doc="""Whether this user's start URL was opened"""
    )

    ip_address = models.GenericIPAddressField(null=True)

    # stores when the page was first visited
    _last_page_timestamp = models.PositiveIntegerField(null=True)

    _last_request_timestamp = models.PositiveIntegerField(null=True)

    is_on_wait_page = models.BooleanField(default=False)

    # these are both for the admin
    # In the changelist, simply call these "page" and "app"
    _current_page_name = models.CharField(max_length=200, null=True,
                                          verbose_name='page')
    _current_app_name = models.CharField(max_length=200, null=True,
                                         verbose_name='app')

    # only to be displayed in the admin participants changelist
    _round_number = models.PositiveIntegerField(
        null=True
    )

    _current_form_page_url = models.URLField()

    _max_page_index = models.PositiveIntegerField()

    _browser_bot_finished = models.BooleanField(default=False)

    _is_bot = models.BooleanField(default=False)

    def player_lookup(self, pages_ahead=0):
        # this is the most reliable way to get the app name,
        # because of WaitUntilAssigned...
        # 2016-04-07: WaitUntilAssigned removed
        try:
            return ParticipantToPlayerLookup.objects.get(
                participant=self.pk,
                page_index=self._index_in_pages + pages_ahead)
        except ParticipantToPlayerLookup.DoesNotExist:
            return

    def get_current_player(self):
        return self.player_lookup().get_player()

    def _current_page(self):
        return '{}/{} pages'.format(self._index_in_pages, self._max_page_index)

    def get_players(self):
        """Used to calculate payoffs"""
        lst = []
        app_sequence = self.session.config['app_sequence']
        for app in app_sequence:
            models_module = otree.common_internal.get_models_module(app)
            players = models_module.Player.objects.filter(
                participant=self
            ).order_by('round_number')
            lst.extend(list(players))
        return lst

    def status(self):
        # TODO: status could be a field that gets set imperatively
        if not self.visited:
            return 'Not started'
        if self.is_on_wait_page:
            if self._waiting_for_ids:
                return 'Waiting for {}'.format(self._waiting_for_ids)
            return 'Waiting'
        return 'Playing'

    def _url_i_should_be_on(self):
        if self._index_in_pages <= self._max_page_index:
            return self.player_lookup().url
        if self.session.mturk_HITId:
            assignment_id = self.mturk_assignment_id
            if self.session.mturk_sandbox:
                url = 'https://workersandbox.mturk.com/mturk/externalSubmit'
            else:
                url = "https://www.mturk.com/mturk/externalSubmit"
            url = otree.common_internal.add_params_to_url(
                url,
                {
                    'assignmentId': assignment_id,
                    'extra_param': '1'  # required extra param?
                }
            )
            return url
        return reverse('OutOfRangeNotification')

    def __unicode__(self):
        return self.name()

    @permalink
    def _start_url(self):
        return 'InitializeParticipant', (self.code,)

    @property
    def payoff(self):
        return sum(player.payoff or c(0) for player in self.get_players())

    def payoff_in_real_world_currency(self):
        return self.payoff.to_real_world_currency(
            self.session
        )

    def payoff_from_subsessions(self):
        """Deprecated on 2015-05-07.
        Remove at some point.
        """
        return self.payoff

    def money_to_pay(self):
        return (
            self.session.config['participation_fee'] +
            self.payoff.to_real_world_currency(self.session)
        )

    def total_pay(self):
        return self.money_to_pay()

    def payoff_is_complete(self):
        return all(p.payoff is not None for p in self.get_players())

    def name(self):
        return id_label_name(self.pk, self.label)
