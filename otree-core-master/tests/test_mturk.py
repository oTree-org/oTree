#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from collections import namedtuple
from django.core.management import call_command
from django.core.urlresolvers import reverse

from otree.models import Session, Participant
from otree.views.mturk import MTurkConnection
import django.test.client
import mock
from mock import MagicMock
from .base import TestCase


class TestMTurk(TestCase):

    def setUp(self):
        call_command('create_session', 'multi_player_game', "9")
        self.session = Session.objects.get()
        self.browser = django.test.client.Client()

    def test_get_create_hit(self):
        url = reverse('MTurkCreateHIT', args=(self.session.code,))
        response = self.browser.get(url, follow=True)
        if response.status_code != 200:
            raise Exception('{} returned 400'.format(url))

    @mock.patch.object(MTurkConnection, '__enter__')
    def test_post_create_hit(self, mocked_enter):
        hit = MagicMock()
        hit.HITId = 'AAA'
        hit.HITGroupId = 'BBB'
        magic = MagicMock()
        magic.create_hit.return_value = [hit]
        mocked_enter.return_value = magic
        url = reverse('MTurkCreateHIT', args=(self.session.code,))
        response = self.browser.post(
            url,
            data={
                'in_sandbox': 'on',
                'title': 'Title for your experiment',
                'description': 'Description for your experiment',
                'keywords': 'easy, bonus, choice, study',
                'money_reward': 10.00,
                'assignments': 6,
                'minutes_allotted_per_assignment': 60,
                'expiration_hours': 168,
            },
            follow=True
        )
        if response.status_code != 200:
            raise Exception('{} returned 400'.format(url))

    @mock.patch.object(MTurkConnection, '__enter__')
    def test_mturk_start(self, mocked_enter):
        mocked_connection = MagicMock()
        mocked_enter.return_value = mocked_connection
        self.session.mturk_qualification_type_id = 'ABCD'
        self.session.save()

        url = reverse('MTurkStart', args=(self.session.code,))
        worker_id = 'WORKER_ID01'
        assignment_id = 'ASSIGNMENT_ID01'
        response = self.browser.get(
            url,
            data={
                'assignmentId': assignment_id,
                'workerId': worker_id
            },
            follow=True
        )
        if response.status_code != 200:
            raise Exception('{} returned 400'.format(url))
        mocked_connection.assign_qualification.assert_called_with(
            self.session.mturk_qualification_type_id,
            worker_id
        )
        p_visitor = Participant.objects.get(
            session=self.session,
            visited=True
        )
        p_non_visitor = Participant.objects.filter(
            session=self.session,
            visited=False
        )[0]

        self.assertTrue(p_visitor.mturk_worker_id == worker_id)
        self.assertTrue(p_visitor.mturk_assignment_id == assignment_id)
        self.assertTrue(p_non_visitor.mturk_worker_id is None)
        self.assertTrue(p_non_visitor.mturk_assignment_id is None)

    def test_mturk_landing_page(self):
        url = reverse('MTurkLandingPage', args=(self.session.code,))
        assignment_id = 'ASSIGNMENT_ID01'
        worker_id = 'WORKER_ID01'
        response = self.browser.get(
            url,
            data={
                'assignmentId': assignment_id,
                'workerId': worker_id
            },
            follow=True
        )
        if response.status_code != 200:
            raise Exception('{} returned 400'.format(url))


Assignment = namedtuple('Assignment', ['WorkerId', 'AssignmentStatus'])


class MockResultSet(list):
    @property
    def TotalNumResults(self):
        return len(self)


class PayMTurk(TestCase):

    def setUp(self):
        call_command('create_session', 'multi_player_game', "9")
        self.session = Session.objects.get()
        self.browser = django.test.client.Client()
        self.participants = self.session.get_participants()

        for (i, p) in enumerate(self.participants):
            p.mturk_worker_id = str(i)
            p.mturk_assignment_id = str(i)
            p.save()

    @mock.patch.object(MTurkConnection, '__enter__')
    def test_pay_mturk(self, mocked_enter):
        assignments = MockResultSet(
            [Assignment(p.mturk_worker_id, 'Submitted') for
             p in self.participants])
        mocked_connection = MagicMock()
        mocked_enter.return_value = mocked_connection
        mocked_connection.get_assignments.return_value = assignments

        url = reverse('MTurkSessionPayments', args=[self.session.code])
        response = self.browser.get(
            url,
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        reject_participants = [p for p in self.participants if p.id % 2]
        accept_participants = [p for p in self.participants if not p.id % 2]

        url = reverse('PayMTurk', args=[self.session.code])
        response = self.browser.post(
            url,
            data={
                'payment': [p.mturk_assignment_id
                            for p in accept_participants],
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        url = reverse('RejectMTurk', args=[self.session.code])
        response = self.browser.post(
            url,
            data={
                'payment': [p.mturk_assignment_id
                            for p in reject_participants],
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
