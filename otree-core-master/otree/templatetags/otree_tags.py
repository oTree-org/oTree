#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# DOCS
# =============================================================================

"""Template tags to for the otree template users.

"""


# =============================================================================
# IMPORTS
# =============================================================================

import decimal

from django import template
from django.template.loader import render_to_string
from django.core.urlresolvers import Resolver404, reverse
from django.utils.safestring import mark_safe

from .otree_forms import FormNode
from .otree_forms import FormFieldNode
from .otree_forms import MarkFieldAsRenderedNode
from .otree_forms import defaultlabel
from otree.common import Currency
import otree.common_internal

import six


# =============================================================================
# CONSTANTS
# =============================================================================

NUMERIC_TYPES = (int, float, complex, decimal.Decimal)

STRING_TYPES = six.string_types

register = template.Library()


# =============================================================================
# TAGS
# =============================================================================

class NextButtonNode(template.Node):
    def render(self, context):
        context.update({})
        try:
            return render_to_string('otree/tags/NextButton.html', context)
        finally:
            context.pop()

    @classmethod
    def parse(cls, parser, tokens):
        return cls()


register.tag('next_button', NextButtonNode.parse)


@register.simple_tag
def active_page(request, view_name, *args, **kwargs):
    if not request:
        return ""
    try:
        url = reverse(view_name, args=args)
        return "active" if url == request.path_info else ""
    except Resolver404:
        return ""


@register.simple_tag
def add_class(var, css_class, *extra_css_classes):
    '''
    tag for specifying css classes
    '''
    try:
        if var or extra_css_classes:
            css_class_template = 'class="%s"'
        else:
            return ''
        css_classes = list(extra_css_classes)
        if var:
            css_classes.append(css_class)
        return css_class_template % ' '.join(css_classes)
    except Resolver404:
        return ""

NO_USER_MSG = '''
Before logging in, you must create a user by setting ADMIN_USERNAME and
ADMIN_PASSWORD in settings.py
'''


@register.simple_tag
def ensure_superuser_exists():
    '''
    Creates a superuser on the fly, so that the user doesn't have to migrate
    or resetdb to get a superuser.
    If eventually we use migrations instead of resetdb, then maybe won't
    need this anymore.
    '''
    success = otree.common_internal.ensure_superuser_exists()
    if success:
        return ''
    return NO_USER_MSG


register.tag('pageform', FormNode.parse)
register.tag('mark_field_as_rendered', MarkFieldAsRenderedNode.parse)
register.tag('formfield', FormFieldNode.parse)

# maybe in the future we rename formfield tag to form_field
# to be more consistent with views.py form_fields=
# adding it now for possible forwards compatibility
register.tag('form_field', FormFieldNode.parse)

# =============================================================================
# FILTERS
# =============================================================================


@register.filter
def c(val):
    return Currency(val)


@register.filter(name="abs")
def abs_value(var):
    return abs(var)


@register.filter(name="repr")
def as_repr(var):
    return repr(var)


@register.filter(name='strip')
def strip(var):
    return var.strip()


@register.filter(name='is_instance')
def is_instance(var, typenames):
    typenames = [tn.strip() for tn in typenames.split(",")]
    return type(var).__name__ in typenames


@register.filter(name='is_numeric')
def is_numeric(var):
    return isinstance(var, NUMERIC_TYPES)


@register.filter(name='is_text')
def is_text(var):
    return isinstance(var, STRING_TYPES)


@register.filter(name='br', is_safe=True)
def br(var):
    result = var.replace("\n", "<br>")
    return mark_safe(result)


register.filter('defaultlabel', defaultlabel)
