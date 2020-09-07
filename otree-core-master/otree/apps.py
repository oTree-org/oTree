#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
from importlib import import_module

from django.apps import AppConfig, apps
from django.conf import settings
from django.db.models import signals

import six

import otree
from otree.models_concrete import UndefinedFormModel, GlobalLockModel
from otree.common_internal import ensure_superuser_exists

logger = logging.getLogger('otree')
import_module('otree.checks')   # this made that style check work


def create_singleton_objects(sender, **kwargs):
    for ModelClass in (UndefinedFormModel, GlobalLockModel):
        # if it doesn't already exist, create one.
        ModelClass.objects.get_or_create()


def monkey_patch_static_tag():
    '''
    In Django >= 1.10, you can use {% load static %}
    instead of {% load staticfiles %}. if we switch to that format,
    then it will bypass this. so eventually after Django 1.10, we
    should change this code to patch django.templatetags.static.static
    '''

    from django.contrib.staticfiles.storage import staticfiles_storage
    from django.contrib.staticfiles.templatetags import staticfiles

    def patched_static(path):
        '''same 1-line function,
        just tries to give a friendlier error message'''
        try:
            return staticfiles_storage.url(path)
        except ValueError as exc:
            msg = '{} - did you remember to run collectstatic?'
            six.reraise(
                ValueError,
                ValueError(msg.format(exc)),
                sys.exc_info()[2])

    staticfiles.static = patched_static


def setup_create_default_superuser():
    authconfig = apps.get_app_config('auth')
    signals.post_migrate.connect(
        ensure_superuser_exists,
        sender=authconfig,
        dispatch_uid='common.models.create_testuser'
    )


def setup_create_singleton_objects():
    signals.post_migrate.connect(create_singleton_objects,
                                 dispatch_uid='create_singletons')


def patch_raven_config():
    # patch settings with info that is only available
    # after other settings loaded
    if hasattr(settings, 'RAVEN_CONFIG'):
        settings.RAVEN_CONFIG['release'] = '{}{}'.format(
            otree.get_version(),
            # need to pass the server if it's DEBUG
            # mode. could do this in extra context or tags,
            # but this seems the most straightforward way
            ',dbg' if settings.DEBUG else ''
        )


class OtreeConfig(AppConfig):
    name = 'otree'
    label = 'otree'
    verbose_name = "oTree"

    def ready(self):
        setup_create_singleton_objects()
        setup_create_default_superuser()
        patch_raven_config()
        monkey_patch_static_tag()
