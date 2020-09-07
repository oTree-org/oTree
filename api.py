from importlib import import_module as _import_module

from otree.models import BaseSubsession, BaseGroup, BasePlayer  # noqa
from otree.constants import BaseConstants  # noqa
from otree.views import Page, WaitPage  # noqa
from otree.common import Currency, currency_range, safe_json  # noqa
from otree.bots import Bot, Submission, SubmissionMustFail, expect  # noqa

models = _import_module('otree.models')
widgets = _import_module('otree.forms.widgets')
