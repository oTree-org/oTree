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
    'CURRENCY_CODE': 'USD',
    'LANGUAGE_CODE': 'en-us',
    'DEBUG': DEBUG,
    'DATABASES': DATABASES,
    'INSTALLED_APPS': [
        'otree',
        '_otree_experiments',
        'raven.contrib.django.raven_compat',
    ],
    'INSTALLED_OTREE_APPS': [

        'lab_results',
        'lying',
        'prisoner',
        'trust',
        'public_goods',
        'dictator',
        'matching_pennies',
        'traveler_dilemma',
        'survey',
        'bargaining',
        'guessing',
        #'quiz',
        'matrix_symmetric',
        'matrix_asymmetric',
        'cournot_competition',
        'stackelberg_competition',
        'private_value_auction',
        'volunteer_dilemma',
        'bertrand_competition',
        'principal_agent',
        'coordination',
        'stag_hunt',
        'battle_of_the_sexes',
        'lemon_market',
        'demo_game',
        'common_value_auction',
        'tragedy_of_the_commons',
        # lab results: displays lab results in a given session

    ],
    'SECRET_KEY': SECRET_KEY,
    'BASE_DIR': BASE_DIR,
    'WSGI_APPLICATION': '_otree_experiments.wsgi.application',
    'ROOT_URLCONF': '_otree_experiments.urls',
}

otree.settings.augment_settings(settings)
