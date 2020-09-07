#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from django.core.management.commands import startapp

import otree
from otree.common_internal import pypi_updates_cli


class Command(startapp.Command):
    def get_default_template(self):
        return os.path.join(
            os.path.dirname(otree.__file__), 'app_template')

    def handle(self, *args, **options):
        if options.get('template', None) is None:
            options['template'] = self.get_default_template()
        super(Command, self).handle(*args, **options)
        try:
            pypi_updates_cli()
        except:  # noqa
            pass  # noqa
        print('Created app folder.')
