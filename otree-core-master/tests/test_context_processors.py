#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six

from django.conf import settings
from django.template import Template, Context

from otree import context_processors

from .base import TestCase


class TestContextProcessors(TestCase):

    def test_otree_context(self):
        template = Template('''{{PAGE_FOOTER|safe}}||{{SEO}}''')
        dctx = context_processors.otree_context(None)
        ctx = Context(dctx)
        rendered = template.render(ctx)
        footer_rendered, seo_rendered = rendered.split("||")
        self.assertEqual(footer_rendered, settings.PAGE_FOOTER)
        self.assertEqual(
            seo_rendered, six.text_type(getattr(settings, "SEO", None) or ()))
