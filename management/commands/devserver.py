import importlib
import os
import os.path
import pathlib
import sys
import termcolor
import time
import traceback
from unittest.mock import patch
from django.conf import settings
from django.core.management import call_command
from pathlib import Path
from django.apps import apps

from . import runserver

TMP_MIGRATIONS_DIR = '__temp_migrations'

ADVICE_DELETE_TMP = (
    "ADVICE: Try deleting the folder {}. If that doesn't work, "
    "look for the error in your models.py."
).format(TMP_MIGRATIONS_DIR)

ADVICE_FIX_NOT_NULL_FIELD = (
    'You may have added a non-nullable field without a default. '
    'This typically happens when importing model fields from django instead of otree.'
)

PRINT_DETAILS_VERBOSITY_LEVEL = 1

ADVICE_PRINT_DETAILS = (
    '(For technical details about this error, run "otree devserver --verbosity=1")'
).format(PRINT_DETAILS_VERBOSITY_LEVEL)

db_engine = settings.DATABASES['default']['ENGINE'].lower()

if 'sqlite' in db_engine:
    ADVICE_DELETE_DB = (
        'ADVICE: Stop the server, '
        'then delete the file db.sqlite3 in your project folder, '
        'then run "otree devserver", not "otree resetdb".'
    )
else:
    if 'postgres' in db_engine:
        db_engine = 'PostgreSQL'
    elif 'mysql' in db_engine:
        db_engine = 'MySQL'

    ADVICE_DELETE_DB = (
        'ADVICE: Delete (drop) your {} database, then create a new empty one '
        'with the same name. "otree devserver" cannot be used on a database '
        'that was generated with "otree resetdb". You should either use one '
        'command or the other.'
    ).format(db_engine)


class Command(runserver.Command):

    inside_runzip = False

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--inside-runzip', action='store_true', dest='inside_runzip', default=False,
        )
    def inner_run(self, *args, inside_runzip, **options):

        self.inside_runzip = inside_runzip
        self.handle_migrations()

        super().inner_run(*args, **options)

    def handle_migrations(self):

        # only get apps with labels, otherwise migrate will raise an error
        # when it tries to migrate that app but no migrations dir was created
        app_labels = set(
            model._meta.app_config.label
            for model in apps.get_models()
        )

        migrations_modules = {
            app_label: '{}.{}'.format(TMP_MIGRATIONS_DIR, app_label)
            for app_label in app_labels
        }

        settings.MIGRATION_MODULES = migrations_modules

        migrations_dir_path = os.path.join(settings.BASE_DIR, TMP_MIGRATIONS_DIR)
        pathlib.Path(TMP_MIGRATIONS_DIR).mkdir(exist_ok=True)

        init_file_path = os.path.join(migrations_dir_path, '__init__.py')
        pathlib.Path(init_file_path).touch(exist_ok=True)

        self.perf_check()

        start = time.time()

        try:
            # makemigrations rarely sends any interesting info to stdout.
            # if there is an error, it will go to stdout,
            # or raise CommandError.
            # if someone needs to see the details of makemigrations,
            # they can do "otree makemigrations".
            with patch('sys.stdout.write'):
                call_command('makemigrations', '--noinput', *migrations_modules.keys())
        except SystemExit as exc:
            # SystemExit will be raised if NonInteractiveMigrationQuestioner
            # cannot decide what to do automatically.
            # SystemExit does not inherit from Exception,
            # so we need to catch it explicitly.
            # without this, the process will just exit and the autoreloader
            # will hang.
            self.print_error_and_exit(ADVICE_FIX_NOT_NULL_FIELD)
        except Exception as exc:
            self.print_error_and_exit(ADVICE_DELETE_TMP)

        # migrate imports some modules that were created on the fly,
        # so according to the docs for import_module, we need to call
        # invalidate_cache.
        # the following line is necessary to avoid a crash I experienced
        # on Mac, because makemigrations tries some imports which cause ImportErrors,
        # messes up the cache on some systems.
        importlib.invalidate_caches()

        try:
            # see above comment about makemigrations and capturing stdout.
            # it applies to migrate command also.
            with patch('sys.stdout.write'):
                # call_command does not add much overhead (0.1 seconds typical)
                call_command('migrate', '--noinput')
        except Exception as exc:
            # it seems there are different exceptions all named
            # OperationalError (django.db.OperationalError,
            # sqlite.OperationalError, mysql....)
            # so, simplest to use the string name

            if type(exc).__name__ in (
                    'OperationalError',
                    'ProgrammingError',
                    'InconsistentMigrationHistory'):
                self.print_error_and_exit(ADVICE_DELETE_DB)
            else:
                raise

        total_time = round(time.time() - start, 1)
        if total_time > 5:
            self.stdout.write('makemigrations & migrate ran in {}s'.format(total_time))

    def print_error_and_exit(self, advice):
        '''this won't actually exit because we can't kill the autoreload process'''
        self.stdout.write('\n')
        is_verbose = self.verbosity >= PRINT_DETAILS_VERBOSITY_LEVEL
        show_error_details = is_verbose or self.inside_runzip
        if show_error_details:
            traceback.print_exc()
        else:
            self.stdout.write('An error occurred.')
        if not self.inside_runzip:
            termcolor.cprint(advice, 'white', 'on_red')
        if not show_error_details:
            self.stdout.write(ADVICE_PRINT_DETAILS)
        sys.exit(0)

    def perf_check(self):
        '''after about 150 migrations,
        load time increased from 0.6 to 1.2+ second'''

        MAX_MIGRATIONS = 200

        # we want to delete migrations files, but keep __init__.py
        # and directories, because then we don't need to
        # migrations files are named 0001_xxx.py, 0002_xxx.py, etc.
        # so, we assume they will all
        file_glob = '{}/*/0*.py'.format(TMP_MIGRATIONS_DIR)
        python_fns = list(Path('.').glob(file_glob))
        num_files = len(python_fns)

        if num_files > MAX_MIGRATIONS:
            advice = (
                'You have too many migrations files ({}). '
                'This can slow down performance. '
                'You should delete the directory {} '
                'and also delete your database.'
            ).format(num_files, TMP_MIGRATIONS_DIR)
            termcolor.cprint(advice, 'white', 'on_red')
