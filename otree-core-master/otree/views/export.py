#!/usr/bin/env python
# -*- coding: utf-8 -*-


# =============================================================================
# IMPORTS
# =============================================================================

import datetime

from django.http import HttpResponse
from django.conf import settings

import vanilla

import otree.common_internal
import otree.models
from otree.common_internal import app_name_format


# =============================================================================
# VIEWS
# =============================================================================

class ExportIndex(vanilla.TemplateView):

    template_name = 'otree/export/index.html'

    url_pattern = r"^export/$"

    def get_context_data(self, **kwargs):
        context = super(ExportIndex, self).get_context_data(**kwargs)
        app_labels = settings.INSTALLED_OTREE_APPS
        app_labels_with_data = []
        for app_label in app_labels:
            model_module = otree.common_internal.get_models_module(app_label)
            if model_module.Player.objects.exists():
                app_labels_with_data.append(app_label)
        apps = [
            {"name": app_name_format(app_label), "label": app_label}
            for app_label in app_labels_with_data
        ]
        context.update({'apps': apps})
        return context


class ExportAppDocs(vanilla.View):

    url_pattern = r"^ExportAppDocs/(?P<app_label>[\w.]+)/$"

    def _doc_file_name(self, app_label):
        return '{} - documentation ({}).txt'.format(
            otree.common_internal.app_name_format(app_label),
            datetime.date.today().isoformat()
        )

    def get(self, request, *args, **kwargs):
        app_label = kwargs['app_label']
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            self._doc_file_name(app_label)
        )
        otree.common_internal.export_docs(response, app_label)
        return response


class ExportCsv(vanilla.View):

    url_pattern = r"^ExportCsv/(?P<app_label>[\w.]+)/$"

    def _data_file_name(self, app_label):
        return '{} (accessed {}).csv'.format(
            otree.common_internal.app_name_format(app_label),
            datetime.date.today().isoformat(),
        )

    def get(self, request, *args, **kwargs):
        app_label = kwargs['app_label']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            self._data_file_name(app_label)
        )
        otree.common_internal.export_data(response, app_label)
        return response


class ExportTimeSpent(vanilla.View):

    url_pattern = r"^ExportTimeSpent/$"

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            'TimeSpent (accessed {}).csv'.format(
                datetime.date.today().isoformat()
            )
        )
        otree.common_internal.export_time_spent(response)
        return response
