#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import asgi_redis
import redis.exceptions
import six


class RedisChannelLayer(asgi_redis.RedisChannelLayer):

    # In SAL experiment, we got 503 "queue full" errors when using ~50
    # browser bots. This occurred even after i enabled multiple botworkers.
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('capacity', 10000)
        super().__init__(*args, **kwargs)
