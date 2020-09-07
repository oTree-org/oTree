#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management import call_command

from otree.models import Session
import django.test.client
from .base import TestCase


class TestSessionAdmin(TestCase):

    def setUp(self):
        call_command('create_session', 'multi_player_game', "9")
        self.session = Session.objects.get()
        self.browser = django.test.client.Client()

    def test_tabs(self):
        tabs = [
            'SessionDescription',
            'SessionMonitor',
            'SessionPayments',
            'SessionResults',
            'SessionStartLinks',
            'AdvanceSession',
            'SessionFullscreen',
        ]
        urls = ['/{}/{}/'.format(PageName, self.session.code) for
                PageName in tabs]

        urls.extend([
            '/sessions/{}/participants/'.format(self.session.code),
        ])

        for url in urls:
            response = self.browser.get(url, follow=True)
            if response.status_code != 200:
                raise Exception('{} returned 400'.format(url))

    def test_edit_session_properties(self):
        path = '/SessionEditProperties/{}/'.format(self.session.code)

        data = {
            'label': 'label_foo',
            'experimenter_name': 'experimenter_name_foo',
            'comment': 'comment_foo',
            'participation_fee': '3.14',
            'real_world_currency_per_point': '0.0314',
        }
        resp = self.browser.post(
            path=path,
            data=data,
            follow=True
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.browser.get(path, follow=True)
        self.assertEqual(resp.status_code, 200)

        html = resp.content.decode('utf-8')
        for val in data.values():
            self.failUnless(val in html)
