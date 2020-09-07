#!/usr/bin/env python
# -*- coding: utf-8 -*-

# deprecation shim
import warnings

from otree.deprecate import OtreeDeprecationWarning

from django.core.management.base import BaseCommand


DEPRECATION_STRING = ('celery command no longer exists in oTree 0.5+. '
                      'You should update your Procfile.')


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        warnings.warn(DEPRECATION_STRING, OtreeDeprecationWarning)
