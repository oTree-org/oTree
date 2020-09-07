#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys

import colorama
from django.apps import AppConfig
from django.conf import settings
from django.db.models import signals

import otree
import otree.common_internal
from otree.common_internal import (
    ensure_superuser_exists
)
from otree.strict_templates import patch_template_silent_failures


logger = logging.getLogger('otree')


def create_singleton_objects(sender, **kwargs):
    from otree.models_concrete import UndefinedFormModel
    for ModelClass in [UndefinedFormModel]:
        # if it doesn't already exist, create one.
        ModelClass.objects.get_or_create()


SQLITE_LOCKING_ADVICE = (
    'Locking is common with SQLite. '
    'When you run your study, you should use a database like PostgreSQL '
    'that is resistant to locking'
)


def monkey_patch_db_cursor():
    '''Monkey-patch the DB cursor, to catch ProgrammingError and
    OperationalError. The alternative is to use middleware, but (1)
    that doesn't catch errors raised outside of views, like channels consumers
    and the task queue, and (2) it's not as specific, because there are
    OperationalErrors that come from different parts of the app that are
    unrelated to resetdb. This is the most targeted location.
    '''


    # In Django 2.0, this method is renamed to _execute.
    # but seems to still work in 2.2?
    def execute(self, sql, params=None):
        self.db.validate_no_broken_transaction()
        with self.db.wrap_database_errors:
            try:
                if params is None:
                    return self.cursor.execute(sql)
                else:
                    return self.cursor.execute(sql, params)
            except Exception as exc:
                ExceptionClass = type(exc)
                # it seems there are different exceptions all named
                # OperationalError (django.db.OperationalError,
                # sqlite.OperationalError, mysql....)
                # so, simplest to use the string name
                if ExceptionClass.__name__ in (
                        'OperationalError', 'ProgrammingError'):
                    # these error messages are localized, so we can't
                    # just check for substring 'column' or 'table'
                    # all the ProgrammingError and OperationalError
                    # instances I've seen so far are related to resetdb,
                    # except for "database is locked"
                    tb = sys.exc_info()[2]
                    if 'locked' in str(exc):
                        advice = SQLITE_LOCKING_ADVICE
                        import django.db.transaction
                    else:
                        advice = 'try resetting the database ("otree resetdb")'

                    raise ExceptionClass('{} - {}.'.format(
                        exc, advice)).with_traceback(tb) from None
                else:
                    raise

    from django.db.backends import utils
    utils.CursorWrapper.execute = execute


def setup_create_default_superuser():
    signals.post_migrate.connect(
        ensure_superuser_exists,
        dispatch_uid='otree.create_superuser'
    )


def setup_create_singleton_objects():
    signals.post_migrate.connect(create_singleton_objects,
                                 dispatch_uid='create_singletons')




class OtreeConfig(AppConfig):
    name = 'otree'
    label = 'otree'
    verbose_name = "oTree"

    def ready(self):
        setup_create_singleton_objects()
        setup_create_default_superuser()
        monkey_patch_db_cursor()
        # to initialize locks

        colorama.init(autoreset=True)

        import otree.checks
        otree.checks.register_system_checks()
        patch_template_silent_failures()


