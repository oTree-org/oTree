#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.test.utils import override_settings

import otree
from otree import apps

from .base import TestCase


class TestApps(TestCase):

    @override_settings(RAVEN_CONFIG={})
    def test_patch_raven_config(self):
        apps.patch_raven_config()
        expected = {
            'release': '{}{}'.format(
                otree.get_version(), ',dbg' if settings.DEBUG else '')}
        self.assertEquals(settings.RAVEN_CONFIG, expected)
