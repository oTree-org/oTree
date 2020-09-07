import csv
import datetime

from django.http import HttpResponse
from django.conf import settings

import vanilla

import otree.common_internal
import otree.models
import otree.export
from otree.models.participant import Participant
from otree.models.session import Session
from otree.extensions import get_extensions_data_export_views
from otree.models_concrete import ChatMessage


class ExportIndex(vanilla.TemplateView):

    template_name = 'otree/admin/Export.html'

    url_pattern = r"^export/$"

    def get_context_data(self, **kwargs):

        # can't use settings.INSTALLED_OTREE_APPS, because maybe the app
        # was removed from SESSION_CONFIGS.
        app_names_with_data = set()
        for session in Session.objects.all():
            for app_name in session.config['app_sequence']:
                app_names_with_data.add(app_name)

        return super().get_context_data(
            db_is_empty=not Participant.objects.exists(),
            app_names=app_names_with_data,
            chat_messages_exist=ChatMessage.objects.exists(),
            extensions_views=get_extensions_data_export_views(),
            **kwargs
        )


class ExportAppDocs(vanilla.View):

    url_pattern = r"^ExportAppDocs/(?P<app_name>[\w.]+)/$"

    def _doc_file_name(self, app_name):
        return '{} - documentation ({}).txt'.format(
            app_name,
            datetime.date.today().isoformat()
        )

    def get(self, request, app_name):
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            self._doc_file_name(app_name)
        )
        otree.export.export_docs(response, app_name)
        return response


def get_export_response(request, file_prefix):
    if bool(request.GET.get('xlsx')):
        content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        file_extension = 'xlsx'
    else:
        content_type = 'text/csv'
        file_extension = 'csv'
    response = HttpResponse(
        content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(
        '{} (accessed {}).{}'.format(
            file_prefix,
            datetime.date.today().isoformat(),
            file_extension
        ))
    return response, file_extension


class ExportApp(vanilla.View):

    url_pattern = r"^ExportApp/(?P<app_name>[\w.]+)/$"

    def get(self, request, app_name):
        response, file_extension = get_export_response(request, app_name)
        otree.export.export_app(app_name, response, file_extension=file_extension)
        return response


class ExportWide(vanilla.View):

    url_pattern = r"^ExportWide/$"

    def get(self, request):
        response, file_extension = get_export_response(
            request, 'All apps - wide')
        otree.export.export_wide(response, file_extension)
        return response


class ExportTimeSpent(vanilla.View):

    url_pattern = r"^ExportTimeSpent/$"

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            'TimeSpent (accessed {}).csv'.format(
                datetime.date.today().isoformat()
            )
        )
        otree.export.export_time_spent(response)
        return response


class ExportChat(vanilla.View):

    url_pattern = '^otreechatcore_export/$'

    def get(self, request):

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            'Chat messages (accessed {}).csv'.format(
                datetime.date.today().isoformat()
            )
        )

        column_names = [
            'participant__session__code',
            'participant__session_id',
            'participant__id_in_session',
            'participant__code',
            'channel',
            'nickname',
            'body',
            'timestamp',
        ]

        rows = ChatMessage.objects.order_by('timestamp').values_list(*column_names)

        writer = csv.writer(response)
        writer.writerows([column_names])
        writer.writerows(rows)

        return response