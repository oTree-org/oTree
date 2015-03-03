import os

import dj_database_url

import otree.settings
#from otree.common import RealWorldCurrency


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
    # Change this to something unique (e.g. mash your keyboard),
    # and then delete this comment.
    SECRET_KEY = 'zzzzzzzzzzzzzzzzzzzzzzzzzzz'


DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}


CREATE_DEFAULT_SUPERUSER = True
ADMIN_USERNAME = 'admin'
AUTH_LEVEL = os.environ.get('OTREE_AUTH_LEVEL')
ACCESS_CODE_FOR_DEFAULT_SESSION = 'idd1610'

# settting for intergration with AWS Mturk
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
MTURK_HOST = 'mechanicalturk.amazonaws.com'
MTURK_SANDBOX_HOST = 'mechanicalturk.sandbox.amazonaws.com'

# e.g. EUR, CAD, GBP, CHF, CNY, JPY
PAYMENT_CURRENCY_CODE = 'USD'
USE_POINTS = True


# e.g. en-gb, de-de, it-it, fr-fr.
# see: https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'


INSTALLED_APPS = [
    'otree',
]

if 'SENTRY_DSN' in os.environ:
    INSTALLED_APPS += [
        'raven.contrib.django.raven_compat',
    ]

SESSION_TYPE_DEFAULTS = {
    'real_world_currency_per_point': 0.01,
    'demo_enabled': True,
    'fixed_pay': 10.00,
    'num_bots': 12,
    'doc': "",
    'group_by_arrival_time': False,
    'mturk_hit_settings': {
        'keywords': ['easy', 'bonus', 'choice', 'study'],
        'title': 'Title for your experiment',
        'description': 'Description for your experiment',
        'frame_height': 500,
        'landing_page_template': 'global/MTurkLanding.html',
    },
}

SESSION_TYPES = [
    {
        'name': 'demo_game',
        'display_name': "Demo Game",
        'num_demo_participants':  1,
        'app_sequence': ['demo_game'],
    },
    {
        'name': 'public_goods',
        'display_name': "Public Goods",
        'num_demo_participants':  3,
        'app_sequence': ['public_goods', 'payment_info'],
    },
    {
        'name': 'principal_agent',
        'display_name': "Principal Agent",
        'num_demo_participants': 2,
        'app_sequence': ['principal_agent', 'feedback', 'payment_info'],
    },
    {
        'name': 'prisoner',
        'display_name': "Prisoner's Dilemma",
        'num_demo_participants': 2,
        'app_sequence': ['prisoner', 'feedback', 'survey_sample', 'payment_info'],
    },
    {
        'name': 'cournot_competition',
        'display_name': "Cournot Competition",
        'num_demo_participants': 2,
        'app_sequence': [
            'cournot_competition', 'survey_sample', 'payment_info'
        ],
    },
    {
        'name': 'trust',
        'display_name': "Trust Game",
        'num_demo_participants': 2,
        'app_sequence': ['trust', 'feedback', 'payment_info'],
    },
    {
        'name': 'ultimatum',
        'display_name': "Ultimatum",
        'num_demo_participants': 2,
        'app_sequence': ['ultimatum', 'feedback', 'payment_info'],
    },
    {
        'name': 'ultimatum_strategy',
        'display_name': "Ultimatum (strategy method treatment)",
        'num_demo_participants': 2,
        'app_sequence': ['ultimatum', 'feedback', 'payment_info'],
        'treatment': 'strategy',
    },
    {
        'name': 'ultimatum_non_strategy',
        'display_name': "Ultimatum (direct response treatment)",
        'num_demo_participants': 2,
        'app_sequence': ['ultimatum', 'feedback', 'payment_info'],
        'treatment': 'direct_response',
    },

    {
        'name': 'dictator',
        'display_name': "Dictator Game",
        'num_demo_participants': 2,
        'app_sequence': ['dictator', 'feedback', 'payment_info'],
    },
    {
        'name': 'matching_pennies',
        'display_name': "Matching Pennies",
        'num_demo_participants': 2,
        'app_sequence': [
            'matching_pennies', 'survey_sample', 'payment_info'
        ],
    },
    {
        'name': 'traveler_dilemma',
        'display_name': "Traveler's Dilemma",
        'num_demo_participants': 2,
        'app_sequence': ['traveler_dilemma', 'feedback', 'payment_info'],
    },
    {
        'name': 'survey',
        'display_name': "Survey",
        'num_demo_participants': 1,
        'app_sequence': ['survey'],
    },
    {
        'name': 'bargaining',
        'display_name': "Bargaining Game",
        'num_demo_participants': 2,
        'app_sequence': ['bargaining', 'payment_info'],
    },
    {
        'name': 'beauty',
        'display_name': "Beauty Contest",
        'num_demo_participants': 5,
        'num_bots': 5,
        'app_sequence': ['beauty', 'survey_sample', 'payment_info'],
    },
    {
        'name': 'common_value_auction',
        'display_name': "Common Value Auction",
        'num_demo_participants': 3,
        'app_sequence': ['common_value_auction', 'payment_info'],
    },
    {
        'name': 'stackelberg_competition',
        'display_name': "Stackelberg Competition",
        'real_world_currency_per_point': 0.01,
        'num_demo_participants': 2,
        'app_sequence': [
            'stackelberg_competition', 'survey_sample', 'payment_info'
        ],
    },
    {
        'name': 'vickrey_auction',
        'display_name': "Vickrey Auction",
        'num_demo_participants': 3,
        'app_sequence': ['vickrey_auction', 'payment_info'],
    },
    {
        'name': 'volunteer_dilemma',
        'display_name': "Volunteer's Dilemma",
        'num_demo_participants': 3,
        'app_sequence': ['volunteer_dilemma', 'feedback', 'payment_info'],
    },
    {
        'name': 'bertrand_competition',
        'display_name': "Bertrand Competition",
        'num_demo_participants': 2,
        'app_sequence': [
            'bertrand_competition', 'feedback', 'payment_info'
        ],
    },
    {
        'name': 'stag_hunt',
        'display_name': "Stag Hunt",
        'num_demo_participants': 2,
        'app_sequence': ['stag_hunt', 'survey_sample', 'payment_info'],
    },
    {
        'name': 'battle_of_the_sexes',
        'display_name': "Battle of the Sexes",
        'num_demo_participants': 2,
        'app_sequence': [
            'battle_of_the_sexes', 'survey_sample', 'payment_info'
        ],
    },
    {
        'name': 'real_effort',
        'display_name': "Real-effort transcription task",
        'num_demo_participants':  1,
        'app_sequence': [
            'real_effort',
        ],
    },
    {
        'name': 'lemon_market',
        'display_name': "Lemon Market Game",
        'num_demo_participants':  3,
        'app_sequence': [
            'lemon_market','payment_info'
        ],
    },
    {
        'name': 'mturk',
        'display_name': "mturk",
        'num_demo_participants':  1,
        'app_sequence': [
            'mturk_submit',
        ],
    },

]


DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            Source code
        </a> for the below games.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Below are various games implemented with oTree. These games are all open
    source, and you can modify them as you wish to create your own variations.
    Click one to learn more and play.
</p>
"""


PAGE_FOOTER = 'Powered By <a href="http://otree.org" target="_blank">oTree</a>'

# list of extra string to positioning you experiments on search engines
# Also if you want to add a particular set of SEO words to a particular page
# add to template context "page_seo" variable.
# See: http://en.wikipedia.org/wiki/Search_engine_optimization
SEO = ()


WSGI_APPLICATION = 'wsgi.application'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

otree.settings.augment_settings(globals())
