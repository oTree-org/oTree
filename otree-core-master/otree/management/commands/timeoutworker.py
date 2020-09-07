#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run the worker to enforce page timeouts
# even if the user closes their browser
from huey.contrib.djhuey.management.commands.run_huey import (
    Command as HueyCommand
)


class Command(HueyCommand):
    def handle(self, *args, **options):
        # clear any tasks in Huey DB, so they don't pile up over time,
        # especially if you run the server without the timeoutworker to consume
        # the tasks.
        # this code is also in asgi.py. it should be in both places,
        # to ensure the database is flushed in all circumstances.
        from huey.contrib.djhuey import HUEY
        HUEY.flush()
        super(Command, self).handle(*args, **options)
