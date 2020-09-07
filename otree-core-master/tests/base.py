#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings

from django.conf import settings
import django.test

# =============================================================================
# HELPER
# =============================================================================


# 2016-06-16: is this still needed? TODO
class OTreeTestClient(django.test.client.Client):

    def login(self):
        return super(OTreeTestClient, self).login(
            username=settings.ADMIN_USERNAME, password=settings.ADMIN_PASSWORD)


class TestCase(django.test.TestCase):

    client_class = OTreeTestClient

    def assertWarns(self, warning, callable, *args, **kwds):
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter('always')

            callable(*args, **kwds)

        condition = any(item.category == warning for item in warning_list)
        msg = "'{}' not warned".format(str(warning))
        self.assertTrue(condition, msg)
