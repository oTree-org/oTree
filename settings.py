import os
import otree.settings
import dj_database_url

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.environ.get('OTREE_PRODUCTION'):
    DEBUG = False
else:
    DEBUG = True

if os.environ.get('IS_OTREE_DOT_ORG'):
    ADMIN_PASSWORD = os.environ['OTREE_ADMIN_PASSWORD']
    SECRET_KEY = os.environ['OTREE_SECRET_KEY']
else:
    ADMIN_PASSWORD = 'otree'
    # don't share this with anybody.
    # Change this to something unique (e.g. mash your keyboard), and then delete this comment.
    SECRET_KEY = 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'



DATABASES = {}
DATABASES['default'] = dj_database_url.config(
    default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
)


CREATE_DEFAULT_SUPERUSER = True
ADMIN_USERNAME = 'admin'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# e.g. EUR, CAD, GBP, CHF, CNY, JPY
CURRENCY_CODE = 'EUR'

# e.g. en-gb, de-de, it-it, fr-fr. see: https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'

INSTALLED_APPS = [
    'otree',
    'raven.contrib.django.raven_compat',
]

INSTALLED_OTREE_APPS = [
    'demo_game',
    'trust',
    'lab_results',
    'public_goods',
    'prisoner',
    'cournot_competition',
    'dictator',
    'matching_pennies',
    'traveler_dilemma',
    'survey',
    'bargaining',
    'guessing',
    'common_value_auction',
    'matrix_symmetric',
    'matrix_asymmetric',
    'stackelberg_competition',
    'private_value_auction',
    'volunteer_dilemma',
    'bertrand_competition',
    'principal_agent',
    'stag_hunt',
    'battle_of_the_sexes',
    'survey_sample',
    'asset_market',
    'lemon_market',
]


WSGI_APPLICATION = 'wsgi.application'

SESSIONS_MODULE = 'sessions'

ACCESS_CODE_FOR_OPEN_SESSION = 'idd1610'

otree.settings.augment_settings(globals())

DISABLED_APPS = [
    ],
