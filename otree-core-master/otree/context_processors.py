#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings


def otree_context(request):
    return {
        "PAGE_FOOTER": settings.PAGE_FOOTER,
        "SEO": getattr(settings, "SEO", None) or ()}
