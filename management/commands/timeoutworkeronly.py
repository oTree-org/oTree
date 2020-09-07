#!/usr/bin/env python

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
        # need to set USE_REDIS = True, because it uses the test client
        # to submit pages, and if the next page has a timeout as well,
        # its timeout task should be queued.
        import otree.common_internal
        otree.common_internal.USE_REDIS = True
        super().handle(*args, **options)
