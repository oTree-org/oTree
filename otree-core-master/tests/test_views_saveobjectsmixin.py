#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from mock import Mock

import idmap.tls

from django.core.management import call_command

from otree.models import Participant, Session
from otree.views.abstract import SaveObjectsMixin

from .base import TestCase


class SaveObjectsMixinTest(TestCase):
    def setUp(self):
        # Mock required model classes from app.
        self.mixin = SaveObjectsMixin()

        class Dummy(object):
            pass
        self.mixin.PlayerClass = Dummy
        self.mixin.GroupClass = Dummy
        self.mixin.SubsessionClass = Dummy

    def test_dont_save_if_no_change(self):
        with self.assertNumQueries(0):
            self.mixin.save_objects()

        call_command('create_session', 'simple_game', '1')
        # Reset cache.
        idmap.tls.init_idmap()

        participant = Participant.objects.get()

        # We keep track of the participant.
        instances = self.mixin._get_save_objects_model_instances()
        self.assertEqual(instances, [participant])

        # But we won't save the participant since we didn't change it.
        with self.assertNumQueries(0):
            self.mixin.save_objects()

    def test_save_if_changed(self):
        call_command('create_session', 'simple_game', '1')
        # Reset cache.
        idmap.tls.init_idmap()

        participant = Participant.objects.get()
        participant.save = Mock()

        self.mixin.save_objects()
        # No change, no save.
        self.assertFalse(participant.save.called)

        participant.time_started = datetime.utcnow()
        self.mixin.save_objects()
        # Has change, then save.
        self.assertTrue(participant.save.called)

    def test_nested_changes(self):
        call_command('create_session', 'simple_game', '1')
        # Reset cache.
        idmap.tls.init_idmap()

        # Query participant via session.
        session = Session.objects.get()
        participant = session.participant_set.get()
        participant.is_on_wait_page = not participant.is_on_wait_page

        # Save participant.
        with self.assertNumQueries(1):
            self.mixin.save_objects()

    def test_with_app_models(self):
        call_command('create_session', 'simple_game', '2')

        from .simple_game.models import Group
        from .simple_game.models import Player
        from .simple_game.models import Subsession

        mixin = SaveObjectsMixin()
        mixin.GroupClass = Group
        mixin.PlayerClass = Player
        mixin.SubsessionClass = Subsession

        # Reset cache.
        idmap.tls.init_idmap()

        players = Player.objects.all()
        self.assertEqual(len(players), 2)

        group = players[0].group
        group.save = Mock()
        group.round_number += 1

        # Query session object to test that it's loaded..
        group.session
        participants = group.session.participant_set.all()

        all_instances = set((
            players[0],
            players[1],
            group,
            group.session,
            participants[0],
            participants[1]))

        self.assertEqual(
            set(mixin._get_save_objects_model_instances()),
            all_instances)

        # No queries are executed. The group model shall be saved, but we
        # mocked out the save method. All other models should be left
        # untouched.
        with self.assertNumQueries(0):
            mixin.save_objects()

        self.assertTrue(group.save.called)
