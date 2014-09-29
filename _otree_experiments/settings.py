import os
import otree.settings

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

# How to set heroku vars: https://devcenter.heroku.com/articles/config-vars
if os.environ.get("HEROKU"):
    import dj_database_url
    DATABASES = {}
    DATABASES['default'] = dj_database_url.config()
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

settings = {
    'CREATE_DEFAULT_SUPERUSER': True,
    'ADMIN_USERNAME': 'admin',
    'ADMIN_PASSWORD': ADMIN_PASSWORD,
    'AWS_ACCESS_KEY_ID': os.environ.get('AWS_ACCESS_KEY_ID'),
    'AWS_SECRET_ACCESS_KEY': os.environ.get('AWS_SECRET_ACCESS_KEY'),
    'CURRENCY_CODE': 'USD', # e.g. EUR, CAD, GBP, CHF, CNY, JPY
    'LANGUAGE_CODE': 'en-us', # e.g. en-gb, de-de, it-it, fr-fr. see: https://docs.djangoproject.com/en/1.6/topics/i18n/
    'DEBUG': DEBUG,
    'DATABASES': DATABASES,
    'INSTALLED_APPS': [
        'otree',
        '_otree_experiments',
        'raven.contrib.django.raven_compat',
    ],
    'INSTALLED_OTREE_APPS': [
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
        'asset_market',

    ],
    'SECRET_KEY': SECRET_KEY,
    'BASE_DIR': BASE_DIR,
    'WSGI_APPLICATION': '_otree_experiments.wsgi.application',
    'ROOT_URLCONF': '_otree_experiments.urls',
}

otree.settings.augment_settings(settings)

# FIXME: convert the below apps to use the new API (remove forms.py)
DISABLED_APPS = [

        'matrix_symmetric',
        'matrix_asymmetric',
        'stackelberg_competition',
        'private_value_auction',
        'volunteer_dilemma',
        'bertrand_competition',
        'principal_agent',
        'coordination',
        'stag_hunt',
        'battle_of_the_sexes',
        'lemon_market',
        'tragedy_of_the_commons',
        # lab results: displays lab results in a given session

    ],