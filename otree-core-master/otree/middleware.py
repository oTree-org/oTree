#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# IMPORTS
# =============================================================================

from django.http import HttpResponseServerError

from otree.common_internal import db_status_ok


class CheckDBMiddleware(object):

    synced = None

    def process_request(self, request):
        if not CheckDBMiddleware.synced:
            CheckDBMiddleware.synced = db_status_ok()
            if not CheckDBMiddleware.synced:
                msg = ("Your database is not ready. "
                       "Try running 'otree resetdb'.")
                return HttpResponseServerError(msg)
