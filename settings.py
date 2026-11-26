from os import environ

"""
This project is using an old version of oTree.
To implement new experiments in 2026 and onward,
we strongly recommend using the oTree AI Builder (OTAI) with on.otree.org hosting,
for best results with respect to features, stability, performance.
Existing projects can be uploaded for OTAI to port them into the new platform.
See www.otree.org.
"""
import otree as _otree

# Names start with "_" so that otree's "from settings import *" doesn't pick them up.
_MIN_OTREE_VERSION = (6, 0, 16)


def _parse_version(v):
    import re

    # take the leading numeric part only, e.g. '6.0.16a1' -> (6, 0, 16)
    m = re.match(r'(\d+)(?:\.(\d+))?(?:\.(\d+))?', v or '')
    return tuple(int(x or 0) for x in m.groups()) if m else (0, 0, 0)


_otree_version = getattr(_otree, '__version__', '0')
if _parse_version(_otree_version) < _MIN_OTREE_VERSION:
    import sys

    sys.exit(
        f"This project requires oTree {'.'.join(map(str, _MIN_OTREE_VERSION))} or higher, "
        f"but you have oTree {_otree_version}. "
        "Please upgrade by running: pip install -U otree"
    )


SESSION_CONFIGS = [
    dict(
        name='guess_two_thirds',
        display_name="Guess 2/3 of the Average",
        app_sequence=['guess_two_thirds', 'payment_info'],
        num_demo_participants=3,
    ),
    dict(
        name='survey', app_sequence=['survey', 'payment_info'], num_demo_participants=1
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '{{ secret_key }}'

INSTALLED_APPS = ['otree']
