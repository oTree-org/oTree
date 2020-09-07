import contextlib
import hashlib
import importlib.util
import logging
import random
import re
import string
import sys
import threading
import uuid
from collections import OrderedDict
from importlib import import_module
from io import StringIO
from channels.layers import get_channel_layer
import otree.channels.utils as channel_utils
import six
from django.apps import apps
from django.conf import settings
from django.db import connection
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from huey.contrib.djhuey import HUEY
from six.moves import urllib
import os
import model_utils


# set to False if using runserver
USE_REDIS = bool(os.environ.get('OTREE_USE_REDIS', ''))

# these locks need to be here rather than views.abstract or views.participant
# because they need to be imported when the main thread runs.
start_link_thread_lock = threading.RLock()
wait_page_thread_lock = threading.RLock()


def add_params_to_url(url, params):
    url_parts = list(urllib.parse.urlparse(url))

    # use OrderedDict because sometimes we want certain params at end
    # for readability/consistency
    query = OrderedDict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.parse.urlencode(query)
    return urllib.parse.urlunparse(url_parts)


SESSION_CODE_CHARSET = string.ascii_lowercase + string.digits


def random_chars(num_chars):
    return ''.join(random.choice(SESSION_CODE_CHARSET) for _ in range(num_chars))


def random_chars_8():
    return random_chars(8)


def random_chars_10():
    return random_chars(10)


def get_models_module(app_name):
    '''shouldn't rely on app registry because the app might have been removed
    from SESSION_CONFIGS, especially if the session was created a long time
    ago and you want to export it'''
    module_name = '{}.models'.format(app_name)
    return import_module(module_name)


def get_bots_module(app_name):
    for module_name in ['tests', 'bots']:
        dotted = '{}.{}'.format(app_name, module_name)
        if importlib.util.find_spec(dotted):
            return import_module(dotted)
    raise ImportError('No tests module found for app {}'.format(app_name))


def get_pages_module(app_name):
    for module_name in ['pages', 'views']:
        dotted = '{}.{}'.format(app_name, module_name)
        if importlib.util.find_spec(dotted):
            return import_module(dotted)
    raise ImportError('No pages module found for app {}'.format(app_name))


def get_app_constants(app_name):
    '''Return the ``Constants`` object of a app defined in the models.py file.

    Example::

        >>> from otree.common_internal import get_app_constants
        >>> get_app_constants('demo')
        <class demo.models.Constants at 0x7fed46bdb188>

    '''
    return get_models_module(app_name).Constants


def get_dotted_name(Cls):
    return '{}.{}'.format(Cls.__module__, Cls.__name__)


def get_app_label_from_import_path(import_path):
    '''App authors must not override AppConfig.label'''
    return import_path.split('.')[-2]


def get_app_label_from_name(app_name):
    '''App authors must not override AppConfig.label'''
    return app_name.split('.')[-1]


def expand_choice_tuples(choices):
    '''allows the programmer to define choices as a list of values rather
    than (value, display_value)

    '''
    if not choices:
        return None
    if not isinstance(choices[0], (list, tuple)):
        choices = [(value, value) for value in choices]
    return choices


def missing_db_tables():
    """Try to execute a simple select * for every model registered
    """

    # need to normalize to lowercase because MySQL converts DB names to lower
    expected_table_names_dict = {
        Model._meta.db_table.lower(): '{}.{}'.format(Model._meta.app_label, Model.__name__)
        for Model in apps.get_models()
    }

    expected_table_names = set(expected_table_names_dict.keys())

    # again, normalize to lowercase
    actual_table_names = set(
        tn.lower() for tn in connection.introspection.table_names())

    missing_table_names = expected_table_names - actual_table_names

    # don't use the SQL table name because it could be uppercase or lowercase,
    # depending on whether it's MySQL
    return [expected_table_names_dict[missing_table]
            for missing_table in missing_table_names]


def make_hash(s):
    s += settings.SECRET_KEY
    return hashlib.sha224(s.encode()).hexdigest()[:8]


def get_admin_secret_code():
    s = settings.SECRET_KEY
    return hashlib.sha224(s.encode()).hexdigest()[:8]

def validate_alphanumeric(identifier, identifier_description):
    if re.match(r'^[a-zA-Z0-9_]+$', identifier):
        return identifier
    raise ValueError(
        '{} "{}" can only contain letters, numbers, '
        'and underscores (_)'.format(
            identifier_description,
            identifier
        )
    )


EMPTY_ADMIN_USERNAME_MSG = 'settings.ADMIN_USERNAME is empty'
EMPTY_ADMIN_PASSWORD_MSG = 'settings.ADMIN_PASSWORD is empty'

def ensure_superuser_exists(*args, **kwargs) -> str:
    """
    Creates our default superuser.
    If it fails, it returns a failure message
    """
    username = settings.ADMIN_USERNAME
    password = settings.ADMIN_PASSWORD
    if not username:
        return EMPTY_ADMIN_USERNAME_MSG
    if not password:
        return EMPTY_ADMIN_PASSWORD_MSG
    from django.contrib.auth.models import User
    if User.objects.filter(username=username).exists():
        # msg = 'Default superuser exists.'
        # logger.info(msg)
        return ''
    User.objects.create_superuser(username, email='', password=password)
    msg = 'Created superuser "{}"'.format(username)
    logging.getLogger('otree').info(msg)
    return ''


def release_any_stale_locks():
    '''
    Need to release locks in case the server was stopped abruptly,
    and the 'finally' block in each lock did not execute
    '''
    from otree.models_concrete import ParticipantLockModel
    for LockModel in [ParticipantLockModel]:
        try:
            LockModel.objects.filter(locked=True).update(locked=False)
        except:
            # if server is started before DB is synced,
            # this will raise
            # django.db.utils.OperationalError: no such table:
            # otree_globallockmodel
            # we can ignore that because we just want to make sure there are no
            # active locks
            pass


def get_redis_conn():
    '''reuse Huey Redis connection'''
    return HUEY.storage.conn

def has_group_by_arrival_time(app_name):
    page_sequence = get_pages_module(app_name).page_sequence
    if len(page_sequence) == 0:
        return False
    return getattr(page_sequence[0], 'group_by_arrival_time', False)


@contextlib.contextmanager
def transaction_except_for_sqlite():
    '''
    On SQLite, transactions tend to result in "database locked" errors.
    So, skip the transaction on SQLite, to allow local dev.
    Should only be used if omitting the transaction rarely causes problems.
    '''
    if settings.DATABASES['default']['ENGINE'].endswith('sqlite3'):
        yield
    else:
        with transaction.atomic():
            yield


class DebugTable(object):
    def __init__(self, title, rows):
        self.title = title
        self.rows = []
        for k, v in rows:
            if isinstance(v, six.string_types):
                v = v.strip().replace("\n", "<br>")
                v = mark_safe(v)
            self.rows.append((k, v))


class InvalidRoundError(ValueError):
    pass


def in_round(ModelClass, round_number, **kwargs):
    if round_number < 1:
        raise InvalidRoundError('Invalid round number: {}'.format(round_number))
    try:
        return ModelClass.objects.get(round_number=round_number, **kwargs)
    except ModelClass.DoesNotExist:
        raise InvalidRoundError(
            'No corresponding {} found with round_number={}'.format(
                ModelClass.__name__, round_number)) from None


def in_rounds(ModelClass, first, last, **kwargs):
    if first < 1:
        raise InvalidRoundError('Invalid round number: {}'.format(first))
    qs = ModelClass.objects.filter(
            round_number__range=(first, last),
            **kwargs
        ).order_by('round_number')

    ret = list(qs)
    num_results = len(ret)
    expected_num_results = last-first+1
    if num_results != expected_num_results:
        raise InvalidRoundError(
            'Database contains {} records for rounds {}-{}, but expected {}'.format(
                num_results, first, last, expected_num_results))
    return ret


class BotError(AssertionError):
    pass


def _get_all_configs():
    return [
        app
        for app in apps.get_app_configs()
        if app.name in settings.INSTALLED_OTREE_APPS]


def participant_start_url(code):
    return '/InitializeParticipant/{}'.format(code)


def patch_migrations_module():
    from django.db.migrations.loader import MigrationLoader
    def migrations_module(*args, **kwargs):
        # need to return None so that load_disk() considers it
        # unmigrated, and False so that load_disk() considers it
        # non-explicit
        return None, False
    MigrationLoader.migrations_module = migrations_module


class ResponseForException(Exception):
    '''
    allows us to show a much simplified traceback without
    framework code.
    '''
    pass

def add_field_tracker(cls):
    # need to do it here because FieldTracker doesnt work on abstract classes
    _ft = model_utils.FieldTracker()
    _ft.contribute_to_class(cls, '_ft')
    # need to call this, because class_prepared has already been fired
    # (it is currently executing)
    _ft.finalize_class(sender=cls)
