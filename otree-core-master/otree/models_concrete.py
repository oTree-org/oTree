#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

from .common_internal import get_models_module


class PageCompletion(models.Model):
    class Meta:
        app_label = "otree"

    app_name = models.CharField(max_length=300)
    page_index = models.PositiveIntegerField()
    page_name = models.CharField(max_length=300)
    time_stamp = models.PositiveIntegerField()
    seconds_on_page = models.PositiveIntegerField()
    subsession_pk = models.PositiveIntegerField()
    participant = models.ForeignKey('otree.Participant')
    session = models.ForeignKey('otree.Session')
    auto_submitted = models.BooleanField()


class PageTimeout(models.Model):
    class Meta:
        app_label = "otree"
        index_together = ['participant', 'page_index']

    participant = models.ForeignKey('otree.Participant')
    page_index = models.PositiveIntegerField()
    expiration_time = models.PositiveIntegerField()


class CompletedGroupWaitPage(models.Model):
    class Meta:
        app_label = "otree"
        unique_together = ['page_index', 'session', 'group_pk']
        index_together = ['page_index', 'session', 'group_pk']

    page_index = models.PositiveIntegerField()
    session = models.ForeignKey('otree.Session')
    group_pk = models.PositiveIntegerField()
    after_all_players_arrive_run = models.BooleanField(default=False)


class CompletedSubsessionWaitPage(models.Model):
    class Meta:
        app_label = "otree"
        unique_together = ['page_index', 'session']
        index_together = ['page_index', 'session']

    page_index = models.PositiveIntegerField()
    session = models.ForeignKey('otree.Session')
    after_all_players_arrive_run = models.BooleanField(default=False)


class ParticipantToPlayerLookup(models.Model):
    class Meta:
        app_label = "otree"
        index_together = ['participant', 'page_index']
        unique_together = ['participant', 'page_index']

    participant = models.ForeignKey('otree.Participant')
    page_index = models.PositiveIntegerField()
    app_name = models.CharField(max_length=300)
    player_pk = models.PositiveIntegerField()
    url = models.CharField(max_length=300)

    def get_player_model(self):
        return getattr(get_models_module(self.app_name), 'Player')

    def get_player(self):
        return self.get_player_model().objects.get(pk=self.player_pk)


class GlobalLockModel(models.Model):
    class Meta:
        app_label = "otree"

    locked = models.BooleanField(default=False)


class ParticipantLockModel(models.Model):
    class Meta:
        app_label = "otree"

    participant_code = models.CharField(
        max_length=16, unique=True
    )

    locked = models.BooleanField(default=False)


class UndefinedFormModel(models.Model):
    """To be used as the model for an empty form, so that form_class can be
    omitted. Consider using SingletonModel for this. Right now, I'm not
    sure we need it.

    """

    class Meta:
        app_label = "otree"

    pass


class RoomToSession(models.Model):
    class Meta:
        app_label = "otree"

    room_name = models.CharField(unique=True, max_length=255)
    session = models.ForeignKey('otree.Session')


FAILURE_MESSAGE_MAX_LENGTH = 300


class FailedSessionCreation(models.Model):
    class Meta:
        app_label = "otree"

    pre_create_id = models.CharField(max_length=100, db_index=True)
    message = models.CharField(max_length=FAILURE_MESSAGE_MAX_LENGTH)


class ParticipantRoomVisit(models.Model):
    class Meta:
        app_label = "otree"

    room_name = models.CharField(max_length=50)
    participant_label = models.CharField(max_length=200)
    tab_unique_id = models.CharField(max_length=20, unique=True)
    last_updated = models.DateTimeField(auto_now=True)


class ExpectedRoomParticipant(models.Model):
    class Meta:
        app_label = "otree"
        unique_together = ['room_name', 'participant_label']

    room_name = models.CharField(max_length=50)
    participant_label = models.CharField(max_length=200)


class BrowserBotsLauncherSessionCode(models.Model):
    class Meta:
        app_label = "otree"

    code = models.CharField(max_length=10)

    # hack to enforce singleton
    is_only_record = models.BooleanField(unique=True, default=True)
