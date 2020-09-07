#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import  # for channels module

import sys

import asgi_redis
import redis.exceptions
import six

REDIS_MSG = (
    "oTree 0.5+ requires Redis to be installed and running, "
    "unless you are using the development server (runserver). "
    "See http://otree.readthedocs.io/en/latest/v0.5.html ."
)


class RedisChannelLayer(asgi_redis.RedisChannelLayer):
    def receive_many(self, channels, block=False):
        try:
            return super(RedisChannelLayer, self).receive_many(channels, block)
        except redis.exceptions.ConnectionError as exception:
            ExceptionClass = type(exception)
            six.reraise(
                ExceptionClass,
                ExceptionClass(REDIS_MSG + ' ' + str(exception)),
                sys.exc_info()[2])

    def new_channel(self, pattern):
        try:
            return super(RedisChannelLayer, self).new_channel(pattern)
        except redis.exceptions.ConnectionError as exception:
            ExceptionClass = type(exception)
            six.reraise(
                ExceptionClass,
                ExceptionClass(REDIS_MSG + ' ' + str(exception)),
                sys.exc_info()[2])
