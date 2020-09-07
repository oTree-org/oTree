import os
import os.path
from django.contrib.messages import constants as messages
import dj_database_url
from otree import __version__

DEFAULT_MIDDLEWARE = (
    'otree.middleware.CheckDBMiddleware',
    'otree.middleware.perf_middleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

SENTRY_DSN = os.environ.get('SENTRY_DSN')
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        # 2018-11-24: breadcrumbs were causing memory leaks when doing queries,
        # especially when creating sessions, which construct hugely verbose
        # queries with bulk_create.
        # however, i could only clearly observe the difference this line makes
        # when testing
        # on a script that bulk_created thousands of non-otree models.
        # when testing on a live server, things are more ambiguous.
        # maybe just refreshing the page several times after creating a session
        # is enough to reset memory to reasnoable levels?
        # disabling also may make things faster...
        # in anecdotal test, 40 vs 50 seconds
        max_breadcrumbs=0,
        release=__version__,
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


def get_default_settings(user_settings: dict):
    '''
    doesn't mutate user_settings, just reads from it
    because some settings depend on others
    '''
    default_settings = {}

    # 2019-04-02: it seems logging works fine inside botworker and channels,
    # without any special logger config.
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
                'formatter': 'simple'
            },
        },
        'loggers': {
            'otree.test.core': {
                'handlers': ['console'],
                'propagate': False,
                'level': 'INFO',
            },
            # but, i should use a logger, because i need to catch exceptions
            # in botworker so it keeps running
            'otree.test.browser_bots': {
                'handlers': ['console'],
                'propagate': False,
                'level': 'INFO',
            },
            'django.request': {
                'handlers': ['console'],
                'propagate': True,
                'level': 'DEBUG',
            },
        }
    }

    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
    BASE_DIR = user_settings.get('BASE_DIR', '')

    # I thought about just checking if REDIS_URL is defined,
    # but using Redis when it's not necessary makes things much slower.
    # for example, running a 5 second bot test takes 22 seconds with Redis.
    # it would be a pain for me to keep setting and unsetting REDIS_URL.
    if os.environ.get('OTREE_USE_REDIS'):
        channel_layer = {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [REDIS_URL],
            }
        }
    else:
        channel_layer = {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        }

    default_settings.update(
        DEBUG=os.environ.get('OTREE_PRODUCTION') in [None, '', '0'],
        AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID'),
        AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        AUTH_LEVEL=os.environ.get('OTREE_AUTH_LEVEL'), DATABASES={
            'default': dj_database_url.config(
                default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
            )
        },
        HUEY={
            'name': 'otree-huey',
            'connection': {
                'url': REDIS_URL,
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
        },
        STATIC_ROOT=os.path.join(BASE_DIR, '__temp_static_root'),
        STATIC_URL='/static/',
        STATICFILES_STORAGE=(
            'whitenoise.storage.CompressedManifestStaticFilesStorage'
        ),
        ROOT_URLCONF='otree.urls',
        TIME_ZONE='UTC',
        USE_TZ=True,
        ALLOWED_HOSTS=['*'],
        LOGGING=logging,
        FORM_RENDERER='django.forms.renderers.TemplatesSetting',
        REAL_WORLD_CURRENCY_CODE='USD',
        REAL_WORLD_CURRENCY_DECIMAL_PLACES=2,
        USE_POINTS=True,
        POINTS_DECIMAL_PLACES=0,
        ADMIN_PASSWORD=os.environ.get('OTREE_ADMIN_PASSWORD', ''),
        USE_L10N=True,
        SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https'),
        ASGI_APPLICATION="otree.channels.routing.application",
        CHANNEL_LAYERS={'default': channel_layer},
        REDIS_URL=REDIS_URL,
        MTURK_NUM_PARTICIPANTS_MULTIPLE=2,
        LOCALE_PATHS=[
            os.path.join(user_settings.get('BASE_DIR', ''), 'locale')
        ],
        BOTS_CHECK_HTML=True
    )
    return default_settings


class InvalidVariableError(Exception):
    pass


class InvalidTemplateVariable(str):
    def get_error_message(self, variable_name_dotted: str):
        bits = variable_name_dotted.split('.')
        if len(bits) == 1:
            return (
                'Invalid variable: "{}". '
                'Maybe you need to return it from vars_for_template()'
            ).format(bits[0])

        built_in_vars = [
            'player',
            'group',
            'subsession',
            'participant',
            'session',
            'Constants',
        ]

        if bits[0] in built_in_vars:
            # This will not make sense in the admin report!
            # but that's OK, it's a rare case, more advanced users
            return (
                '{} has no attribute "{}"'
            ).format(bits[0], '.'.join(bits[1:]))
        elif bits[0] == 'self' and bits[1] in built_in_vars:
            return (
                "Don't use 'self' in the template. "
                "Just write: {}"
            ).format('.'.join(bits[1:]))
        else:
            return 'Invalid variable: {}'.format(variable_name_dotted)

    def __mod__(self, other):
        '''hack that takes advantage of string_if_invalid's %s behavior'''
        msg = self.get_error_message(str(other))
        # "from None" because otherwise we get the full chain of
        # checking if it's an attribute, dict key, list index ...
        raise InvalidVariableError(msg) from None


def validate_user_settings(settings: dict):
    '''
    These are the settings that from my testing must not be None.
    This just exists so that oTree doesn't give a cryptic error later on
    '''

    # currently not using the datatypes, maybe do that later
    required_settings = {
        'SESSION_CONFIG_DEFAULTS': dict,
        'SESSION_CONFIGS': list,
        'LANGUAGE_CODE': str,
        'SECRET_KEY': str,
        'ADMIN_USERNAME': str,
    }
    for SETTING in required_settings:
        if SETTING not in settings:
            raise ValueError(f'Required setting {SETTING} is missing from settings.py.')
        elif settings.get(SETTING) is None:
            raise ValueError(f'settings.py: setting {SETTING} cannot be None.')


def augment_settings(settings: dict):
    validate_user_settings(settings)
    default_settings = get_default_settings(settings)
    for k, v in default_settings.items():
        settings.setdefault(k, v)

    all_otree_apps_set = set()

    for s in settings['SESSION_CONFIGS']:
        for app in s['app_sequence']:
            all_otree_apps_set.add(app)

    all_otree_apps = list(all_otree_apps_set)

    no_experiment_apps = [
        'otree',

        # django.contrib.auth is slow, about 300ms.
        # would be nice to only add it if there is actually a password
        # i tried that but would need to add various complicated "if"s
        # throughout the code
        'django.contrib.auth',
        'django.forms',
        # needed for auth and very quick to load
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        # need to keep this around indefinitely for all the people who
        # have {% load static %}
        'django.contrib.staticfiles',
        'channels',
        'huey.contrib.djhuey',
        'idmap',
    ]

    if os.environ.get('OTREE_SECRET_KEY'):
        # then override the SECRET_KEY from settings file, which might
        # be exposed if the source code is made public
        # an alternative is to change the project template so that
        # SECRET_KEY = os.environ.get('OTREE_SECRET_KEY', '{{ secret_key }}')
        # but this change is just as good and backward compatible
        # and doesn't involve any churn.
        # people don't usually care about the specific value of their secret key.
        # eventually maybe we can make SECRET_KEY an optional setting,
        # but that will require people to set the env vars.
        settings['SECRET_KEY'] = os.environ['OTREE_SECRET_KEY']

    # order is important:
    # otree unregisters User & Group, which are installed by auth.
    # otree templates need to get loaded before the admin.
    no_experiment_apps = collapse_to_unique_list(
        no_experiment_apps,
        settings['INSTALLED_APPS'],
        settings.get('EXTENSION_APPS', [])
    )

    new_installed_apps = collapse_to_unique_list(
        no_experiment_apps, all_otree_apps)

    # TEMPLATES
    _template_dir = os.path.join(settings['BASE_DIR'], '_templates')
    if os.path.exists(_template_dir):
        new_template_dirs = [_template_dir]
    else:
        new_template_dirs = []

    # STATICFILES
    _static_dir = os.path.join(settings['BASE_DIR'], '_static')

    if os.path.exists(_static_dir):
        additional_static_dirs = [_static_dir]
    else:
        additional_static_dirs = []

    new_staticfiles_dirs = collapse_to_unique_list(
        settings.get('STATICFILES_DIRS'),
        additional_static_dirs,
    )

    new_middleware = collapse_to_unique_list(
        DEFAULT_MIDDLEWARE,
        settings.get('MIDDLEWARE'))

    augmented_settings = dict(
        INSTALLED_APPS=new_installed_apps,
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': new_template_dirs,
            'APP_DIRS': True,
            'OPTIONS': {
                'debug': True,
                'string_if_invalid': InvalidTemplateVariable("%s"),
                'context_processors': (
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.contrib.messages.context_processors.messages',
                    'django.template.context_processors.request',
                )
            },
        }],
        STATICFILES_DIRS=new_staticfiles_dirs,
        MIDDLEWARE=new_middleware,
        INSTALLED_OTREE_APPS=all_otree_apps,
        MESSAGE_TAGS={messages.ERROR: 'danger'},
        LOGIN_REDIRECT_URL='Sessions'
    )

    settings.update(augmented_settings)
