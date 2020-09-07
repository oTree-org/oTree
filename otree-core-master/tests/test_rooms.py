#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
import django.test.client
import unittest
from otree.session import create_session
from .utils import get_path


def has_header(response, header_name):
    return header_name in response


def is_wait_page(response):
    return has_header(response, 'oTree-Wait-Page')


def get_html(response):
    return response.content.decode('utf-8')


def participant_initialized(response):
    print('redirect chain', response.redirect_chain)
    redirect_chain = [ele[0] for ele in response.redirect_chain]
    return any('InitializeParticipant' in url for url in redirect_chain)


class RoomTestCase(unittest.TestCase):
    '''Subclassed from unittest.TestCase,
    because we don't want to flush the participant labels from the DB
    after each test, because it circumvents room._participant_labels_loaded.
    '''

    def setUp(self):
        self.browser = django.test.client.Client()

    def get(self, url):
        resp = self.browser.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.path = get_path(resp, url)
        return resp

    def post(self, url, data=None):
        data = data or {}
        resp = self.browser.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.path = get_path(resp, url)
        return resp


class TestRoomWithoutSession(RoomTestCase):

    def setUp(self):
        self.browser = django.test.client.Client()

    def test_open_admin_links(self):
        urls = [
            reverse('Rooms'),
            reverse('RoomWithoutSession', args=['default']),
            reverse('RoomWithoutSession', args=['anon']),
        ]

        for url in urls:
            self.get(url)

    def test_open_participant_links(self):
        room_with_labels = reverse('AssignVisitorToRoom', args=['default'])

        resp = self.get(room_with_labels)
        self.assertIn('Please enter your participant label', get_html(resp))

        resp = self.get(
            room_with_labels + '?participant_label=JohnSmith',
        )

        self.assertIn('room/default', self.path)

        resp = self.browser.get(
            room_with_labels + '?participant_label=NotInLabelsFile',
        )
        self.assertEqual(resp.status_code, 404)

        anon_base_url = reverse('AssignVisitorToRoom', args=['anon'])

        resp = self.get(anon_base_url)
        self.assertIn('Waiting for your session to begin', get_html(resp))

        resp = self.get(anon_base_url + '?participant_label=JohnSmith')
        self.assertIn('Waiting for your session to begin', get_html(resp))

    def test_ping(self):
        pass


class TestRoomWithSession(RoomTestCase):
    def setUp(self):
        self.browser = django.test.client.Client()
        create_session(
            'single_player_game',
            num_participants=6,
            room_name='default',
        )

        create_session(
            'single_player_game',
            num_participants=6,
            room_name='anon',
        )

    def test_open_admin_links(self):
        self.get(reverse('RoomWithoutSession', args=['default']))
        self.assertTrue('room_with_session' in self.path)

    def test_open_participant_links(self):
        room_with_labels = reverse('AssignVisitorToRoom', args=['default'])

        resp = self.get(room_with_labels)
        self.assertIn('Please enter your participant label', get_html(resp))

        resp = self.get(
            room_with_labels + '?participant_label=JohnSmith',
        )
        self.assertTrue(participant_initialized(resp))

        resp = self.browser.get(
            room_with_labels + '?participant_label=NotInLabelsFile',
        )
        self.assertEqual(resp.status_code, 404)

        anon_base_url = reverse('AssignVisitorToRoom', args=['anon'])

        resp = self.get(anon_base_url)
        self.assertTrue(participant_initialized(resp))

        resp = self.get(anon_base_url + '?participant_label=JohnSmith')
        self.assertTrue(participant_initialized(resp))

    def test_close_room(self):

        url = reverse('CloseRoom', args=['default'])
        self.get(url)

        self.get(reverse('RoomWithoutSession', args=['default']))
        self.assertTrue('room_without_session' in self.path)

    def test_delete_session_in_room(self):
        pass

    def test_session_start_links_room(self):
        pass

    def tearDown(self):
        url = reverse('CloseRoom', args=['default'])
        self.get(url)

        url = reverse('CloseRoom', args=['anon'])
        self.get(url)
