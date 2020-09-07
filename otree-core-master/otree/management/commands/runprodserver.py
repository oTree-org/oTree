#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management import call_command
from . import webandworkers


class Command(webandworkers.Command):

    '''
    It's almost the same as webandworkers,
    but it also runs collectstatic,
    and launches the timeoutworker.
    this command is intended for generic server deployment,
    whereas webandworkers is intended for Heroku.
    '''

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        ahelp = (
            'By default we will collect all static files into the directory '
            'configured in your settings. Disable it with this switch if you '
            'want to do it manually.')
        parser.add_argument(
            '--no-collectstatic', action='store_false', dest='collectstatic',
            default=True, help=ahelp)

    def get_honcho_manager(self, options):
        manager = super(Command, self).get_honcho_manager(options)

        manager.add_process(
            'timeoutworker',
            'otree timeoutworker',
            quiet=False,
            env=self.get_env(options)
        )

        return manager

    def handle(self, *args, **options):
        collectstatic = options['collectstatic']

        if collectstatic:
            self.stdout.write('Running collectstatic ...', ending='')
            call_command('collectstatic', interactive=False, verbosity=1)

        return super(Command, self).handle(*args, **options)
