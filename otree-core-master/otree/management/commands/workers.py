#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from django.core.management.base import BaseCommand

from honcho.manager import Manager


class Command(BaseCommand):
    help = 'Will run channels workers'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '-n', '--num-workers', action='store',
            dest='num_workers', default=6, type=int,
            help='Number of worker processes')

    def get_env(self, options):
        return os.environ.copy()

    def handle(self, *args, **options):
        manager = Manager()

        for i in range(options['num_workers']):
            manager.add_process(
                'worker{}'.format(i),
                'otree runworker',
                quiet=False,
                env=self.get_env(options))

        manager.loop()
        sys.exit(manager.returncode)
