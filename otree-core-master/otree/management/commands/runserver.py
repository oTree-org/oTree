#!/usr/bin/env python
# -*- coding: utf-8 -*-

from channels.management.commands import runserver
import otree.bots.browser
from django.conf import settings
import otree.common_internal


class Command(runserver.Command):

    def handle(self, *args, **options):
        # use in-memory.
        # this is the simplest way to patch runserver to use in-memory,
        # while still using Redis in production
        settings.CHANNEL_LAYERS['default'] = (
            settings.CHANNEL_LAYERS['inmemory'])

        from otree.common_internal import release_any_stale_locks
        release_any_stale_locks()

        # don't use cached template loader, so that users can refresh files
        # and see the update.
        # kind of a hack to patch it here and to refer it as [0],
        # but can't think of a better way.
        settings.TEMPLATES[0]['OPTIONS']['loaders'] = {
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        }

        # so we know not to use Huey
        otree.common_internal.USE_REDIS = False

        # initialize browser bot worker in process memory
        otree.bots.browser.browser_bot_worker = otree.bots.browser.Worker()

        super(Command, self).handle(*args, **options)
