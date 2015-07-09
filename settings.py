import os

import dj_database_url
from boto.mturk import qualification

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# OTREE_PRODUCTION just controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if os.environ.get('OTREE_PRODUCTION') in {None, '', '0'}:
    DEBUG = True
else:
    DEBUG = False

# IS_OTREE_DOT_ORG is only used on demo.otree.org.
# you can assume it is None/''/0.
if os.environ.get('IS_OTREE_DOT_ORG') in {None, '', '0'}:
    ADMIN_PASSWORD = 'otree'
    # don't share this with anybody.
    # Change this to something unique (e.g. mash your keyboard),
    # and then delete this comment.
    SECRET_KEY = 'zzzzzzzzzzzzzzzzzzzzzzzzzzz'
else:
    # ignore the next 2 lines;
    # only used on demo.otree.org
    ADMIN_PASSWORD = os.environ['OTREE_ADMIN_PASSWORD']
    SECRET_KEY = os.environ['OTREE_SECRET_KEY']

PAGE_FOOTER = ''

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}


ADMIN_USERNAME = 'admin'

# AUTH_LEVEL:
# If you are launching an experiment and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to EXPERIMENT.

# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

AUTH_LEVEL = os.environ.get('OTREE_AUTH_LEVEL')

# ACCESS_CODE_FOR_DEFAULT_SESSION:
# If you have a "default session" set,
# then an access code will be appended to the URL for authentication.
# You can change this as frequently as you'd like,
# to prevent unauthorized server access.

ACCESS_CODE_FOR_DEFAULT_SESSION = 'my_access_code'

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
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

# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24, # 7 days
    #'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        qualification.LocaleRequirement("EqualTo", "US"),
        qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 50),
        qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 5),
        #qualification.Requirement('YOUR_QUALIFICATION_ID_HERE', 'DoesNotExist')
    ]
}

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.01,
    'participation_fee': 10.00,
    'num_bots': 12,
    'doc': "",
    'group_by_arrival_time': False,
    'mturk_hit_settings': mturk_hit_settings
}

SESSION_CONFIGS = [
    {
        'name': 'public_goods',
        'display_name': "Public Goods",
        'num_demo_participants': 3,
        'app_sequence': ['public_goods', 'payment_info'],
    },
    {
        'name': 'public_goods_simple',
        'display_name': "Public Goods (simple version from tutorial)",
        'num_demo_participants': 3,
        'app_sequence': ['public_goods_simple', 'survey', 'payment_info'],
    },
    {
        'name': 'trust',
        'display_name': "Trust Game",
        'num_demo_participants': 2,
        'app_sequence': ['trust', 'payment_info'],
    },
    {
        'name': 'trust_simple',
        'display_name': "Trust Game (simple version from tutorial)",
        'num_demo_participants': 2,
        'app_sequence': ['trust_simple'],
    },
    {
        'name': 'beauty',
        'display_name': "Beauty Contest",
        'num_demo_participants': 5,
        'num_bots': 5,
        'app_sequence': ['beauty', 'payment_info'],
    },
    {
        'name': 'survey',
        'display_name': "Survey",
        'num_demo_participants': 1,
        'app_sequence': ['survey', 'payment_info'],
    },
    {
        'name': 'prisoner',
        'display_name': "Prisoner's Dilemma",
        'num_demo_participants': 2,
        'app_sequence': ['prisoner', 'payment_info'],
    },
    {
        'name': 'ultimatum',
        'display_name': "Ultimatum (randomized: strategy vs. direct response)",
        'num_demo_participants': 2,
        'app_sequence': ['ultimatum', 'payment_info'],
    },
    {
        'name': 'ultimatum_strategy',
        'display_name': "Ultimatum (strategy method treatment)",
        'num_demo_participants': 2,
        'app_sequence': ['ultimatum', 'payment_info'],
        'treatment': 'strategy',
    },
    {
        'name': 'ultimatum_non_strategy',
        'display_name': "Ultimatum (direct response treatment)",
        'num_demo_participants': 2,
        'app_sequence': ['ultimatum', 'payment_info'],
        'treatment': 'direct_response',
    },
    {
        'name': 'battle_of_the_sexes',
        'display_name': "Battle of the Sexes",
        'num_demo_participants': 2,
        'app_sequence': [
            'battle_of_the_sexes', 'payment_info'
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
        'app_sequence': ['volunteer_dilemma', 'payment_info'],
    },
    {
        'name': 'cournot_competition',
        'display_name': "Cournot Competition",
        'num_demo_participants': 2,
        'app_sequence': [
            'cournot_competition', 'payment_info'
        ],
    },
    {
        'name': 'principal_agent',
        'display_name': "Principal Agent",
        'num_demo_participants': 2,
        'app_sequence': ['principal_agent', 'payment_info'],
    },
    {
        'name': 'dictator',
        'display_name': "Dictator Game",
        'num_demo_participants': 2,
        'app_sequence': ['dictator', 'payment_info'],
    },
    {
        'name': 'matching_pennies',
        'display_name': "Matching Pennies",
        'num_demo_participants': 2,
        'app_sequence': [
            'matching_pennies', 'payment_info'
        ],
    },
    {
        'name': 'matching_pennies_tutorial',
        'display_name': "Matching Pennies (tutorial version)",
        'num_demo_participants': 2,
        'app_sequence': [
            'matching_pennies_tutorial',
        ],
    },
    {
        'name': 'traveler_dilemma',
        'display_name': "Traveler's Dilemma",
        'num_demo_participants': 2,
        'app_sequence': ['traveler_dilemma', 'payment_info'],
    },
    {
        'name': 'bargaining',
        'display_name': "Bargaining Game",
        'num_demo_participants': 2,
        'app_sequence': ['bargaining', 'payment_info'],
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
            'stackelberg_competition', 'payment_info'
        ],
    },
    {
        'name': 'bertrand_competition',
        'display_name': "Bertrand Competition",
        'num_demo_participants': 2,
        'app_sequence': [
            'bertrand_competition', 'payment_info'
        ],
    },
    {
        'name': 'stag_hunt',
        'display_name': "Stag Hunt",
        'num_demo_participants': 2,
        'app_sequence': ['stag_hunt', 'payment_info'],
    },
    {
        'name': 'real_effort',
        'display_name': "Real-effort transcription task",
        'num_demo_participants': 1,
        'app_sequence': [
            'real_effort',
        ],
    },
    {
        'name': 'lemon_market',
        'display_name': "Lemon Market Game",
        'num_demo_participants': 3,
        'app_sequence': [
            'lemon_market', 'payment_info'
        ],
    },
]


otree.settings.augment_settings(globals())
