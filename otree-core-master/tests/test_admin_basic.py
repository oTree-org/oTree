#!/usr/bin/env python
# -*- coding: utf-8 -*-

import django.test.client
from .base import TestCase
from django.conf import settings
from .utils import get_path


class TestAdminBasic(TestCase):

    def setUp(self):
        self.browser = django.test.client.Client()

    def test_admin_basic(self):
        for tab in [
            'demo',
            'sessions',
            'rooms',
            'create_session',
            'server_check',
            'accounts/login'
        ]:
            response = self.browser.get('/{}/'.format(tab), follow=True)
            self.assertEqual(response.status_code, 200)

    def test_login(self):
        login_url = '/accounts/login/'
        resp = self.browser.post(
            login_url,
            data={
                'username': settings.ADMIN_USERNAME,
                'password': settings.ADMIN_PASSWORD,
            },
            follow=True
        )

        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(login_url, get_path(resp, if_no_redirect=login_url))
