#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path

from django.conf import global_settings
from django.contrib.messages import constants as messages

from six.moves.urllib import parse as urlparse


DEFAULT_MIDDLEWARE_CLASSES = (
    'otree.middleware.CheckDBMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # this middlewware is for generate human redeable errors

    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # 2015-04-08: disabling SSLify until we make this work better
    # 'sslify.middleware.SSLifyMiddleware',
)


def collapse_to_unique_list(*args):
    """Create a new list with all elements from a given lists without reapeated
    elements

    """
    combined = []
    for arg in args:
        for elem in arg or ():
            if elem not in combined:
                combined.append(elem)
    return combined


def get_default_settings(initial_settings=None):
    if initial_settings is None:
        initial_settings = {}
    logging = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        'formatters': {
            'verbose': {
                'format': '[%(levelname)s|%(asctime)s] %(name)s > %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
            'sentry': {
                'level': 'WARNING',
                'class': (
                    'raven.contrib.django.raven_compat.handlers.'
                    'SentryHandler'
                ),
            },
        },
        'loggers': {
            'otree.test.core': {
                'handlers': ['console'],
                'propagate': False,
                'level': 'INFO',
            },
            # 2016-07-25: botworker seems to be sending messages to Sentry
            # without any special configuration, not sure why.
            # but, i should use a logger, because i need to catch exceptions
            # in botworker so it keeps running
            'otree.test.browser_bots': {
                'handlers': ['sentry', 'console'],
                'propagate': False,
                'level': 'INFO',
            },
            'django.request': {
                'handlers': ['console'],
                'propagate': True,
                'level': 'DEBUG',
            },
            # logger so that we can explicitly send certain warnings to sentry,
            # without raising an exception.
            'otree.sentry': {
                'handlers': ['sentry'],
                'propagate': True,
                'level': 'DEBUG',
            },
            # This is required for exceptions inside Huey tasks to get logged
            # to Sentry
            'huey.consumer': {
                'handlers': ['sentry', 'console'],
                'level': 'INFO'
            },
            # suppress the INFO message: 'raven is not configured (logging
            # disabled).....', in case someone doesn't have a DSN
            'raven.contrib.django.client.DjangoClient': {
                'handlers': ['console'],
                'level': 'WARNING'
            }


        }
    }

    page_footer = (
        'Powered By <a href="http://otree.org" target="_blank">oTree</a>'
    )

    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

    return {
        # set to True so that if there is an error in an {% include %}'d
        # template, it doesn't just fail silently. instead should raise
        # an error (and send through Sentry etc)
        'STATIC_ROOT': os.path.join(
            initial_settings.get('BASE_DIR', ''),
            '_static_root'),
        'STATIC_URL': '/static/',
        'STATICFILES_STORAGE': (
            'whitenoise.django.GzipManifestStaticFilesStorage'
        ),
        'ROOT_URLCONF': 'otree.default_urls',

        'TIME_ZONE': 'UTC',
        'USE_TZ': True,
        'ALLOWED_HOSTS': ['*'],

        # SEO AND FOOTER
        'PAGE_FOOTER': page_footer,

        # list of extra string to positioning you experiments on search engines
        # Also if you want to add a particular set of SEO words to a particular
        # page add to template context "page_seo" variable.
        # See: http://en.wikipedia.org/wiki/Search_engine_optimization
        'SEO': (),

        'LOGGING': logging,

        'REAL_WORLD_CURRENCY_CODE': 'USD',
        'REAL_WORLD_CURRENCY_LOCALE': 'en_US',
        'REAL_WORLD_CURRENCY_DECIMAL_PLACES': 2,
        'USE_POINTS': True,

        'POINTS_DECIMAL_PLACES': 0,

        # eventually can remove this,
        # when it's present in otree-library
        # that most people downloaded
        'USE_L10N': True,
        'SECURE_PROXY_SSL_HEADER': ('HTTP_X_FORWARDED_PROTO', 'https'),
        'MTURK_HOST': 'mechanicalturk.amazonaws.com',
        'MTURK_SANDBOX_HOST': 'mechanicalturk.sandbox.amazonaws.com',

        # The project can override the routing.py used as entry point by
        # setting CHANNEL_DEFAULT_ROUTING.

        # 'CHANNEL_LAYERS': {
        #     'default': {
        #         'BACKEND': 'channels.database_layer.DatabaseChannelLayer',
        #         'ROUTING': initial_settings.get(
        #             'CHANNEL_DEFAULT_ROUTING',
        #             'otree.channels.default_routing.channel_routing'),
        #     },
        # },

        'CHANNEL_LAYERS': {
            'default': {
                "BACKEND": "otree.channels.asgi_redis.RedisChannelLayer",
                "CONFIG": {
                    "hosts": [REDIS_URL],
                },
                'ROUTING': initial_settings.get(
                    'CHANNEL_DEFAULT_ROUTING',
                    'otree.channels.default_routing.channel_routing'),
            },
            'inmemory': {
                "BACKEND": "asgiref.inmemory.ChannelLayer",
                'ROUTING': initial_settings.get(
                    'CHANNEL_DEFAULT_ROUTING',
                    'otree.channels.default_routing.channel_routing'),
            },
        },

        # for convenience within oTree
        'REDIS_URL': REDIS_URL,

        # since workers on Amazon MTurk can return the hit
        # we need extra participants created on the
        # server.
        # The following setting is ratio:
        # num_participants_server / num_participants_mturk
        'MTURK_NUM_PARTICIPANTS_MULTIPLE': 2,
        'LOCALE_PATHS': [
            os.path.join(initial_settings.get('BASE_DIR', ''), 'locale')
        ],

        # ideally this would be a per-app setting, but I don't want to
        # pollute Constants. It doesn't make as much sense per session config,
        # so I'm just going the simple route and making it a global setting.
        'BOTS_CHECK_HTML': True,
    }


def augment_settings(settings):

    if 'POINTS_CUSTOM_NAME' in settings:
        settings.setdefault(
            'POINTS_CUSTOM_FORMAT',
            '{} ' + settings['POINTS_CUSTOM_NAME']
        )

    all_otree_apps_set = set()

    if ('SESSION_CONFIGS' not in settings and
            'SESSION_TYPES' in settings):
        raise ValueError(
            'In settings.py, you should rename '
            'SESSION_TYPES to SESSION_CONFIGS, and '
            'SESSION_TYPE_DEFAULTS to SESSION_CONFIG_DEFAULTS.'
        )

    for s in settings['SESSION_CONFIGS']:
        for app in s['app_sequence']:
            all_otree_apps_set.add(app)

    all_otree_apps = list(all_otree_apps_set)

    no_experiment_apps = [
        'django.contrib.auth',
        'otree',
        'floppyforms',
        # need this for admin login
        'django.contrib.admin',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'otree.timeout',
        'channels',
        'huey.contrib.djhuey',
        'rest_framework',
        'idmap',
    ]

    if settings.get('SENTRY_DSN'):
        settings.setdefault(
            'RAVEN_CONFIG',
            {
                'dsn': settings['SENTRY_DSN'],
                'processors': ['raven.processors.SanitizePasswordsProcessor'],
            }
        )
        no_experiment_apps.append('raven.contrib.django.raven_compat')

    # order is important:
    # otree unregisters User & Group, which are installed by auth.
    # otree templates need to get loaded before the admin.
    no_experiment_apps = collapse_to_unique_list(
        no_experiment_apps,
        settings['INSTALLED_APPS']
    )

    new_installed_apps = collapse_to_unique_list(
        no_experiment_apps, all_otree_apps)

    additional_template_dirs = []
    template_dir = os.path.join(settings['BASE_DIR'], 'templates')
    # 2015-09-21: i won't put a deprecation warning because 'templates/'
    # is the django convention and someone might legitimately want it.
    # just remove this code at some point
    # same for static/ dir below
    if os.path.exists(template_dir):
        additional_template_dirs = [template_dir]

    _template_dir = os.path.join(settings['BASE_DIR'], '_templates')
    if os.path.exists(_template_dir):
        additional_template_dirs = [_template_dir]

    new_template_dirs = collapse_to_unique_list(
        settings.get('TEMPLATE_DIRS'),
        # 2015-5-2: 'templates' is deprecated in favor of '_templates'
        # remove it at some point
        additional_template_dirs,
    )

    static_dir = os.path.join(settings['BASE_DIR'], 'static')
    additional_static_dirs = []
    if os.path.exists(static_dir):
        additional_static_dirs = [static_dir]

    _static_dir = os.path.join(settings['BASE_DIR'], '_static')
    if os.path.exists(_static_dir):
        additional_static_dirs = [_static_dir]

    new_staticfiles_dirs = collapse_to_unique_list(
        settings.get('STATICFILES_DIRS'),
        # 2015-5-2: 'static' is deprecated in favor of '_static'
        # remove it at some point
        additional_static_dirs,
    )

    new_middleware_classes = collapse_to_unique_list(
        DEFAULT_MIDDLEWARE_CLASSES,
        settings.get('MIDDLEWARE_CLASSES'))

    augmented_settings = {
        'INSTALLED_APPS': new_installed_apps,
        'TEMPLATES': [{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': new_template_dirs,
            'OPTIONS': {
                'debug': False,
                'loaders': [
                    ('django.template.loaders.cached.Loader', [
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                    ]),
                ],
                'context_processors': collapse_to_unique_list(
                    global_settings.TEMPLATE_CONTEXT_PROCESSORS, (
                        'django.core.context_processors.request',
                        'otree.context_processors.otree_context',
                    )
                ),
            },
        }],
        'STATICFILES_DIRS': new_staticfiles_dirs,
        'MIDDLEWARE_CLASSES': new_middleware_classes,
        'NO_EXPERIMENT_APPS': no_experiment_apps,
        'INSTALLED_OTREE_APPS': all_otree_apps,
        'MESSAGE_TAGS': {messages.ERROR: 'danger'},
        'LOGIN_REDIRECT_URL': 'Sessions',
    }

    settings.setdefault('LANGUAGE_CODE', global_settings.LANGUAGE_CODE)

    CURRENCY_LOCALE = settings.get('REAL_WORLD_CURRENCY_LOCALE', None)
    if not CURRENCY_LOCALE:

        # favor en_GB currency formatting since it represents negative amounts
        # with minus signs rather than parentheses
        # if settings['LANGUAGE_CODE'][:2] == 'en':
        #     CURRENCY_LOCALE = 'en_GB'
        # else:
        CURRENCY_LOCALE = settings['LANGUAGE_CODE']

        settings.setdefault('REAL_WORLD_CURRENCY_LOCALE',
                            CURRENCY_LOCALE.replace('-', '_'))

    overridable_settings = get_default_settings(settings)

    settings.update(augmented_settings)

    for k, v in overridable_settings.items():
        settings.setdefault(k, v)

    redis_url = urlparse.urlparse(settings.get('REDIS_URL'))

    settings['HUEY'] = {
        'name': 'otree-huey',
        'connection': {
            'host': redis_url.hostname,
            'port': redis_url.port,
            'password': redis_url.password
        },
        'always_eager': False,
        # I need a result store to retrieve the results of browser-bots
        # tasks and pinging, even if the result is evaluated immediately
        # (otherwise, calling the task returns None.
        'result_store': False,
        'consumer': {
            'workers': 1,
            # 'worker_type': 'thread',
            'scheduler_interval': 5,
            'loglevel': 'warning',
        },
    }
