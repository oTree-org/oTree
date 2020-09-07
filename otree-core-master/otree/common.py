"""oTree Public API utilities"""

import json
from decimal import Decimal

from django.conf import settings
from django.utils import formats, numberformat
from django.utils.safestring import mark_safe
from django.utils.translation import ungettext

import six

import easymoney


# =============================================================================
# MONKEY PATCH - fix for https://github.com/oTree-org/otree-core/issues/387
# =============================================================================

# Black Magic: The original number format of django used inside templates don't
# work if the currency code contains non-ascii characters. This ugly hack
# remplace the original number format and when you has a easy_money instance
# simple use the old unicode casting.

_original_number_format = numberformat.format


def otree_number_format(number, *args, **kwargs):
    if isinstance(number, easymoney.Money):
        return six.text_type(number)
    return _original_number_format(number, *args, **kwargs)

numberformat.format = otree_number_format


# =============================================================================
# CLASSES
# =============================================================================

class RealWorldCurrency(easymoney.Money):
    '''payment currency'''

    CODE = settings.REAL_WORLD_CURRENCY_CODE
    LOCALE = settings.REAL_WORLD_CURRENCY_LOCALE
    DECIMAL_PLACES = settings.REAL_WORLD_CURRENCY_DECIMAL_PLACES

    __hash__ = Decimal.__hash__

    def __neg__(self):
        cls = type(self)
        val = super(RealWorldCurrency, self).__neg__()
        return cls(val)

    def __pos__(self):
        cls = type(self)
        val = super(RealWorldCurrency, self).__pos__()
        return cls(val)

    def __abs__(self):
        if self < 0:
            return -self
        return self

    def __pow__(self, other):
        cls = type(self)
        val = super(RealWorldCurrency, self).__pow__(other)
        return cls(val)

    def to_number(self):
        return Decimal(self)

    # temporary fix for https://github.com/oTree-org/otree-core/issues/444
    def __repr__(self):
        return 'Currency({})'.format(self)

    def to_real_world_currency(self, session):
        return self

    def deconstruct(self):
        return [
            '{}.{}'.format(self.__module__, self.__class__.__name__),
            [Decimal.__str__(self)], {}]


class Currency(RealWorldCurrency):
    '''game currency'''

    if settings.USE_POINTS:
        DECIMAL_PLACES = settings.POINTS_DECIMAL_PLACES

        @classmethod
        def _format_currency(cls, number):

            formatted_number = formats.number_format(number)

            if hasattr(settings, 'POINTS_CUSTOM_FORMAT'):
                return settings.POINTS_CUSTOM_FORMAT.format(formatted_number)

            # Translators: display a number of points,
            # like "1 point", "2 points", ...
            # See "Plural-Forms" above for pluralization rules
            # in this language.
            # Explanation at http://bit.ly/1IurMu7
            # In most languages, msgstr[0] is singular,
            # and msgstr[1] is plural
            # the {} represents the number;
            # don't forget to include it in your translation
            return ungettext('{} point', '{} points', number).format(
                formatted_number)

        def to_real_world_currency(self, session):
            return RealWorldCurrency(
                self.to_number() *
                session.config['real_world_currency_per_point'])


class _CurrencyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, easymoney.Money):
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
