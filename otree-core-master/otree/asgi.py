#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import  # for channels module
import os
import channels.asgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from otree.common_internal import (
    release_any_stale_locks, get_redis_conn  # noqa
)
release_any_stale_locks()

# clear any tasks in Huey DB, so they don't pile up over time,
# especially if you run the server without the timeoutworker to consume the
# tasks.
# ideally we would only schedule a task in Huey if timeoutworker is running,
# so that we don't pile up messages that never get consumed, but I don't know
# how and when to check if Huey is running, in a performant way.
# this code is also in timeoutworker.
from huey.contrib.djhuey import HUEY  # noqa
HUEY.flush()

from otree.bots.browser import redis_flush_bots  # noqa
redis_flush_bots(get_redis_conn())

channel_layer = channels.asgi.get_channel_layer()
