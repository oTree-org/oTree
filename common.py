"""oTree Public API utilities"""

import json
from decimal import Decimal

from django.conf import settings
from django.utils import formats, numberformat
from django.utils.safestring import mark_safe
from otree.currency import Currency, RealWorldCurrency
import six


# =============================================================================
# MONKEY PATCH - fix for https://github.com/oTree-org/otree-core/issues/387
# =============================================================================

# Black Magic: The original number format of django used inside templates don't
# work if the currency code contains non-ascii characters. This ugly hack
# remplace the original number format and when you has a easy_money instance
# simple use the old unicode casting.

_original_number_format = numberformat.format


def otree_number_format(number, *args, **kwargs):
    if isinstance(number, (Currency, RealWorldCurrency)):
        return six.text_type(number)
    return _original_number_format(number, *args, **kwargs)

numberformat.format = otree_number_format




class _CurrencyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Currency, RealWorldCurrency)):
            if obj.get_num_decimal_places() == 0:
                return int(obj)
            return float(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def safe_json(obj):
    return mark_safe(json.dumps(obj, cls=_CurrencyEncoder))


def currency_range(first, last, increment):
    assert last >= first
    if Currency(increment) == 0:
        if settings.USE_POINTS:
            setting_name = 'POINTS_DECIMAL_PLACES'
        else:
            setting_name = 'REAL_WORLD_CURRENCY_DECIMAL_PLACES'
        raise ValueError(
            ('currency_range() step argument must not be zero. '
             'Maybe your {} setting is '
             'causing it to be rounded to 0.').format(setting_name)
        )

    assert increment > 0  # not negative

    values = []
    current_value = Currency(first)

    while True:
        if current_value > last:
            return values
        values.append(current_value)
        current_value += increment
