#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import collections
import sys
import itertools
import os
import json
from collections import OrderedDict

from six.moves import range
from six.moves import zip

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.urlresolvers import reverse
from django.forms.forms import pretty_name
from django.conf import settings
from django.contrib import messages
from django.utils.encoding import force_text

import vanilla

from ordered_set import OrderedSet as oset

import channels

import easymoney

import otree.constants_internal
from otree.common_internal import (
    create_session_and_redirect, db_status_ok, check_pypi_for_updates)
from otree.session import SESSION_CONFIGS_DICT, create_session, SessionConfig
from otree import forms
from otree.forms import widgets
from otree.common import RealWorldCurrency
from otree.views.abstract import GenericWaitPageMixin, AdminSessionPageMixin
from otree.views.mturk import MTurkConnection, get_workers_by_status
from otree.common import Currency as c
from otree.models import Participant, Session
from otree.models_concrete import (
    PageCompletion, ParticipantRoomVisit, BrowserBotsLauncherSessionCode)
from otree.room import ROOM_DICT


def get_all_fields(Model, for_export=False):
    if Model is PageCompletion:
        return [
            'session_id',
            'participant__id_in_session',
            'participant__code',
            'page_index',
            'app_name',
            'page_name',
            'time_stamp',
            'seconds_on_page',
            'subsession_pk',
            'auto_submitted',
        ]

    if Model is Session:
        return [
            'code',
            'label',
            'experimenter_name',
            'real_world_currency_per_point',
            'time_scheduled',
            'time_started',
            'mturk_HITId',
            'mturk_HITGroupId',
            'participation_fee',
            'comment',
            'is_demo',
            'use_cli_bots',
        ]

    if Model is Participant:
        if for_export:
            return [
                'id_in_session',
                'code',
                'label',
                '_current_page',
                '_current_app_name',
                '_round_number',
                '_current_page_name',
                'ip_address',
                'time_started',
                'exclude_from_data_analysis',
                'visited',
                'mturk_worker_id',
                'mturk_assignment_id',
            ]
        else:
            return [
                '_id_in_session',
                'code',
                'label',
                '_current_page',
                '_current_app_name',
                '_round_number',
                '_current_page_name',
                'status',
                '_last_page_timestamp',
            ]

    first_fields = {
        'Player':
            [
                'id_in_group',
                'role',
            ],
        'Group':
            [
                'id',
            ],
        'Subsession':
            [],
    }[Model.__name__]
    first_fields = oset(first_fields)

    last_fields = {
        'Player': [],
        'Group': [],
        'Subsession': [],
    }[Model.__name__]
    last_fields = oset(last_fields)

    fields_for_export_but_not_view = {
        'Player': {'id', 'label', 'subsession', 'session'},
        'Group': {'id'},
        'Subsession': {'id', 'round_number'},
    }[Model.__name__]

    fields_for_view_but_not_export = {
        'Player': set(),
        'Group': {'subsession', 'session'},
        'Subsession': {'session'},
    }[Model.__name__]

    fields_to_exclude_from_export_and_view = {
        'Player': {
            '_index_in_game_pages',
            'participant',
            'group',
            'subsession',
            'session',
            'round_number',
        },
        'Group': {
            'subsession',
            'id_in_subsession',
            'session',
            '_is_missing_players',
            'round_number',
        },
        'Subsession': {
            'code',
            'label',
            'session',
            'session_access_code',
        },
    }[Model.__name__]

    if for_export:
        fields_to_exclude = fields_to_exclude_from_export_and_view.union(
            fields_for_view_but_not_export
        )
    else:
        fields_to_exclude = fields_to_exclude_from_export_and_view.union(
            fields_for_export_but_not_view
        )

    all_fields_in_model = oset([field.name for field in Model._meta.fields])

    middle_fields = (
        all_fields_in_model - first_fields - last_fields - fields_to_exclude
    )

    return list(first_fields | middle_fields | last_fields)


def get_display_table_rows(app_name, for_export, subsession_pk=None):
    if not for_export and not subsession_pk:
        raise ValueError("if this is for the admin results table, "
                         "you need to specify a subsession pk")
    models_module = otree.common_internal.get_models_module(app_name)
    Player = models_module.Player
    Group = models_module.Group
    Subsession = models_module.Subsession
    if for_export:
        model_order = [
            Participant,
            Player,
            Group,
            Subsession,
            Session
        ]
    else:
        model_order = [
            Player,
            Group,
            Subsession,
        ]

    # get title row
    all_columns = []
    for Model in model_order:
        field_names = get_all_fields(Model, for_export)
        columns_for_this_model = [
            (Model, field_name) for field_name in field_names
            ]
        all_columns.extend(columns_for_this_model)

    if subsession_pk:
        # we had a strange result on one person's heroku instance
        # where Meta.ordering on the Player was being ingnored
        # when you use a filter. So we add one explicitly.
        players = Player.objects.filter(
            subsession_id=subsession_pk).order_by('pk')
    else:
        players = Player.objects.all()
    session_ids = set([player.session_id for player in players])

    # initialize
    parent_objects = {}

    parent_models = [
        Model for Model in model_order if Model not in {Player, Session}
        ]

    for Model in parent_models:
        parent_objects[Model] = {
            obj.pk: obj
            for obj in Model.objects.filter(session_id__in=session_ids)
            }

    if Session in model_order:
        parent_objects[Session] = {
            obj.pk: obj for obj in Session.objects.filter(pk__in=session_ids)
            }

    all_rows = []
    for player in players:
        row = []
        for column in all_columns:
            Model, field_name = column
            if Model == Player:
                model_instance = player
            else:
                fk_name = Model.__name__.lower()
                parent_object_id = getattr(player, "{}_id".format(fk_name))
                if parent_object_id is None:
                    model_instance = None
                else:
                    model_instance = parent_objects[Model][parent_object_id]

            attr = getattr(model_instance, field_name, '')
            if isinstance(attr, collections.Callable):
                if Model == Player and field_name == 'role' \
                        and model_instance.group is None:
                    attr = ''
                else:
                    try:
                        attr = attr()
                    except:
                        attr = "(error)"
            row.append(attr)
        all_rows.append(row)

    values_to_replace = {None: '', True: 1, False: 0}

    for row in all_rows:
        for i in range(len(row)):
            value = row[i]
            try:
                replace = value in values_to_replace
            except TypeError:
                # if it's an unhashable data type
                # like Json or Pickle field
                replace = False
            if replace:
                value = values_to_replace[value]
            elif for_export and isinstance(value, easymoney.Money):
                # remove currency formatting for easier analysis
                value = easymoney.to_dec(value)
            value = force_text(value)
            value = value.replace('\n', ' ').replace('\r', ' ')
            row[i] = value

    column_display_names = []
    for Model, field_name in all_columns:
        column_display_names.append(
            (Model.__name__, field_name)
        )

    return column_display_names, all_rows


class CreateSessionForm(forms.Form):
    session_configs = SESSION_CONFIGS_DICT.values()
    session_config_choices = (
        [('', '-----')] +
        [(s['name'], s['display_name']) for s in session_configs])

    session_config = forms.ChoiceField(
        choices=session_config_choices, required=True)

    num_participants = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        for_mturk = kwargs.pop('for_mturk')
        super(CreateSessionForm, self).__init__(*args, **kwargs)
        if for_mturk:
            self.fields['num_participants'].label = "Number of workers"
            self.fields['num_participants'].help_text = (
                'Since workers can return the hit or drop out '
                '"spare" participants will be created. Namely server will '
                'have %s times more participants than MTurk HIT. '
                'The number you enter in this field is number of '
                'workers required for your HIT.'
                % settings.MTURK_NUM_PARTICIPANTS_MULTIPLE
            )
        else:
            self.fields['num_participants'].label = "Number of participants"

    def clean_num_participants(self):
        session_config_name = self.cleaned_data.get('session_config')

        # We must check for an empty string in case validation is not run
        if session_config_name != '':
            lcm = SESSION_CONFIGS_DICT[session_config_name].get_lcm()
            num_participants = self.cleaned_data['num_participants']
            if num_participants % lcm:
                raise forms.ValidationError(
                    'Please enter a valid number of participants.'
                )
            return num_participants


class CreateSession(vanilla.FormView):
    form_class = CreateSessionForm
    template_name = 'otree/admin/CreateSession.html'

    url_pattern = r"^create_session/$"

    def dispatch(self, request, *args, **kwargs):
        self.for_mturk = (int(self.request.GET.get('mturk', 0)) == 1)
        return super(CreateSession, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        session_config_summaries = [
            session_config.get_info()
            for session_config in SESSION_CONFIGS_DICT.values()]
        kwargs.update({'session_config_summaries': session_config_summaries})
        return super(CreateSession, self).get_context_data(**kwargs)

    def get_form(self, data=None, files=None, **kwargs):
        kwargs['for_mturk'] = self.for_mturk
        return super(CreateSession, self).get_form(data, files, **kwargs)

    def form_valid(self, form):

        session_kwargs = {
            'session_config_name': form.cleaned_data['session_config'],
            'for_mturk': self.for_mturk
        }
        if self.for_mturk:
            session_kwargs['num_participants'] = (
                form.cleaned_data['num_participants'] *
                settings.MTURK_NUM_PARTICIPANTS_MULTIPLE
            )

        else:
            session_kwargs['num_participants'] = (
                form.cleaned_data['num_participants'])

        # TODO:
        # Refactor when we upgrade to push
        if hasattr(self, "room"):
            session_kwargs['room_name'] = self.room.name

        return create_session_and_redirect(session_kwargs)


class Rooms(vanilla.TemplateView):
    template_name = 'otree/admin/Rooms.html'

    url_pattern = r"^rooms/$"

    def get_context_data(self, **kwargs):
        return {'rooms': ROOM_DICT.values()}


class RoomWithoutSession(CreateSession):
    template_name = 'otree/admin/RoomWithoutSession.html'
    room = None

    url_pattern = r"^room_without_session/(?P<room_name>.+)/$"

    def dispatch(self, request, *args, **kwargs):
        self.room = ROOM_DICT[kwargs['room_name']]
        if self.room.has_session():
            return HttpResponseRedirect(
                reverse('RoomWithSession', args=[kwargs['room_name']]))
        return super(RoomWithoutSession, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'participant_urls': self.room.get_participant_urls(self.request),
            'room_wide_url': self.room.get_room_wide_url(self.request),
            'room': self.room,
            'collapse_links': True,
        }
        kwargs.update(context)

        return super(RoomWithoutSession, self).get_context_data(**kwargs)

    def socket_url(self):
        return '/room_without_session/{}/'.format(self.room.name)


class RoomWithSession(vanilla.TemplateView):
    template_name = 'otree/admin/RoomWithSession.html'
    room = None

    url_pattern = r"^room_with_session/(?P<room_name>.+)/$"

    def dispatch(self, request, *args, **kwargs):
        self.room = ROOM_DICT[kwargs['room_name']]
        if not self.room.has_session():
            return HttpResponseRedirect(
                reverse('RoomWithoutSession', args=[kwargs['room_name']]))
        return super(RoomWithSession, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'participant_urls': self.room.get_participant_urls(self.request),
            'room_wide_url': self.room.get_room_wide_url(self.request),
            'session_url': reverse(
                'SessionMonitor',
                args=(self.room.session.code,)),
            'room': self.room,
            'collapse_links': True,
        }
        kwargs.update(context)

        return super(RoomWithSession, self).get_context_data(**kwargs)


class CloseRoom(vanilla.View):
    url_pattern = r"^CloseRoom/(?P<room_name>.+)/$"

    def dispatch(self, request, *args, **kwargs):
        # TODO: should make this POST not GET,
        # but then have to refactor the HTML button
        room_name = kwargs['room_name']
        self.room = ROOM_DICT[room_name]
        self.room.session = None
        # in case any failed to be cleared through regular ws.disconnect
        ParticipantRoomVisit.objects.filter(
            room_name=room_name,
        ).delete()
        return HttpResponseRedirect(
            reverse('RoomWithoutSession', args=[room_name]))


class WaitUntilSessionCreated(GenericWaitPageMixin, vanilla.GenericView):

    url_pattern = r"^WaitUntilSessionCreated/(?P<pre_create_id>.+)/$"

    body_text = 'Waiting until session created'

    def _is_ready(self):
        try:
            self.session = Session.objects.get(
                _pre_create_id=self._pre_create_id
            )
            return True
        except Session.DoesNotExist:
            return False

    def _response_when_ready(self):
        session = self.session
        if session.is_for_mturk():
            session_home_url = reverse(
                'MTurkCreateHIT', args=(session.code,)
            )
        # demo mode
        elif self.request.GET.get('fullscreen'):
            session_home_url = reverse(
                'SessionFullscreen', args=(session.code,))
        else:  # typical case
            session_home_url = reverse(
                'SessionStartLinks', args=(session.code,))

        return HttpResponseRedirect(session_home_url)

    def dispatch(self, request, *args, **kwargs):
        self._pre_create_id = kwargs['pre_create_id']
        return super(WaitUntilSessionCreated, self).dispatch(
            request, *args, **kwargs
        )

    def socket_url(self):
        return '/wait_for_session/{}/'.format(self._pre_create_id)


class SessionFullscreen(AdminSessionPageMixin, vanilla.TemplateView):
    '''Launch the session in fullscreen mode
    only used in demo mode
    '''

    def get_context_data(self, **kwargs):
        '''Get the URLs for the IFrames'''
        context = super(SessionFullscreen, self).get_context_data(**kwargs)
        participant_urls = [
            self.request.build_absolute_uri(participant._start_url())
            for participant in self.session.get_participants()
        ]
        context.update({
            'session': self.session,
            'participant_urls': participant_urls
        })
        return context


class SessionStartLinks(AdminSessionPageMixin, vanilla.TemplateView):

    def get_context_data(self, **kwargs):
        session = self.session
        room = session.get_room()

        context = super(SessionStartLinks, self).get_context_data(**kwargs)

        sqlite = settings.DATABASES['default']['ENGINE'].endswith('sqlite3')
        context.update({
            'use_browser_bots': session.use_browser_bots,
            'sqlite': sqlite,
            'runserver': 'runserver' in sys.argv
        })

        session_start_urls = [
            self.request.build_absolute_uri(participant._start_url())
            for participant in session.get_participants()
        ]

        # TODO: Bot URLs, and a button to start the bots

        if room:
            context.update(
                {
                    'participant_urls':
                        room.get_participant_urls(self.request),
                    'room_wide_url': room.get_room_wide_url(self.request),
                    'session_start_urls': session_start_urls,
                    'room': room,
                    'collapse_links': True,
                })
        else:
            anonymous_url = self.request.build_absolute_uri(
                reverse(
                    'JoinSessionAnonymously',
                    args=(session._anonymous_code,)
                )
            )

            context.update({
                'participant_urls': session_start_urls,
                'anonymous_url': anonymous_url,
                'num_participants': len(session_start_urls),
                'fullscreen_mode_on': len(session_start_urls) <= 3
            })

        return context


class SessionMonitor(AdminSessionPageMixin, vanilla.TemplateView):

    def get_context_data(self, **kwargs):

        field_names = get_all_fields(Participant)
        display_names = {
            '_id_in_session': 'ID in session',
            'code': 'Code',
            'label': 'Label',
            '_current_page': 'Page',
            '_current_app_name': 'App',
            '_round_number': 'Round',
            '_current_page_name': 'Page name',
            'status': 'Status',
            '_last_page_timestamp': 'Time on page',
        }

        column_names = [display_names[col] for col in field_names]

        context = super(SessionMonitor, self).get_context_data(**kwargs)
        context.update({'column_names': column_names})
        return context


class SessionEditPropertiesForm(forms.ModelForm):
    participation_fee = forms.RealWorldCurrencyField(
        required=False,
        # it seems that if this is omitted, the step defaults to an integer,
        # meaninng fractional inputs are not accepted
        widget=widgets.RealWorldCurrencyInput(attrs={'step': 0.01})
    )
    real_world_currency_per_point = forms.DecimalField(
        decimal_places=5, max_digits=12,
        required=False
    )

    class Meta:
        model = Session
        fields = [
            'label',
            'experimenter_name',
            'comment',
        ]


class SessionEditProperties(AdminSessionPageMixin, vanilla.UpdateView):

    # required for vanilla.UpdateView
    lookup_field = 'code'
    model = Session
    form_class = SessionEditPropertiesForm
    template_name = 'otree/admin/SessionEditProperties.html'

    def get_form(self, data=None, files=None, **kwargs):
        form = super(
            SessionEditProperties, self
        ).get_form(data, files, **kwargs)
        config = self.session.config
        form.fields[
            'participation_fee'
        ].initial = config['participation_fee']
        form.fields[
            'real_world_currency_per_point'
        ].initial = config['real_world_currency_per_point']
        if self.session.mturk_HITId:
            form.fields['participation_fee'].widget.attrs['readonly'] = 'True'
        return form

    def get_success_url(self):
        return reverse('SessionEditProperties', args=(self.session.code,))

    def form_valid(self, form):
        super(SessionEditProperties, self).form_valid(form)
        participation_fee = form.cleaned_data[
            'participation_fee'
        ]
        real_world_currency_per_point = form.cleaned_data[
            'real_world_currency_per_point'
        ]
        config = self.session.config
        if form.cleaned_data['participation_fee'] is not None:
            config[
                'participation_fee'
            ] = RealWorldCurrency(participation_fee)
        if form.cleaned_data['real_world_currency_per_point'] is not None:
            config[
                'real_world_currency_per_point'
            ] = real_world_currency_per_point
        self.session.save()
        messages.success(self.request, 'Properties have been updated')
        return HttpResponseRedirect(self.get_success_url())


class SessionPayments(AdminSessionPageMixin, vanilla.TemplateView):

    def get(self, *args, **kwargs):
        response = super(SessionPayments, self).get(*args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        session = self.session
        # TODO: mark which ones are bots
        participants = session.get_participants()
        total_payments = 0.0
        mean_payment = 0.0
        if participants:
            total_payments = sum(
                part.money_to_pay() or c(0) for part in participants
            )
            mean_payment = total_payments / len(participants)

        context = super(SessionPayments, self).get_context_data(**kwargs)
        context.update({
            'participants': participants,
            'total_payments': total_payments,
            'mean_payment': mean_payment,
            'participation_fee': session.config['participation_fee'],
        })

        return context


class MTurkSessionPayments(AdminSessionPageMixin, vanilla.TemplateView):

    def get(self, *args, **kwargs):
        response = super(MTurkSessionPayments, self).get(*args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = super(MTurkSessionPayments, self).get_context_data(**kwargs)
        session = self.session
        if not session.mturk_HITId:
            context.update({'not_published_yet': True})
            return context
        with MTurkConnection(
                self.request, session.mturk_sandbox
        ) as mturk_connection:
            workers_by_status = get_workers_by_status(
                mturk_connection,
                session.mturk_HITId
            )
            participants_not_reviewed = session.participant_set.filter(
                mturk_worker_id__in=workers_by_status['Submitted']
            )
            participants_approved = session.participant_set.filter(
                mturk_worker_id__in=workers_by_status['Approved']
            )
            participants_rejected = session.participant_set.filter(
                mturk_worker_id__in=workers_by_status['Rejected']
            )

        context.update({
            'participants_approved': participants_approved,
            'participants_rejected': participants_rejected,
            'participants_not_reviewed': participants_not_reviewed,
            'participation_fee': session.config['participation_fee'],
        })

        return context


class SessionResults(AdminSessionPageMixin, vanilla.TemplateView):

    def get_context_data(self, **kwargs):
        session = self.session

        participants = session.get_participants()
        participant_labels = [p._id_in_session() for p in participants]
        column_name_tuples = []
        rows = []

        for subsession in session.get_subsessions():
            app_label = subsession._meta.app_config.name

            column_names, subsession_rows = get_display_table_rows(
                subsession._meta.app_config.name,
                for_export=False,
                subsession_pk=subsession.pk
            )

            if not rows:
                rows = subsession_rows
            else:
                for i in range(len(rows)):
                    rows[i].extend(subsession_rows[i])

            round_number = subsession.round_number
            if round_number > 1:
                subsession_column_name = '{} [Round {}]'.format(
                    app_label, round_number
                )
            else:
                subsession_column_name = app_label

            for model_column_name, field_column_name in column_names:
                column_name_tuples.append(
                    (subsession_column_name,
                     model_column_name,
                     field_column_name)
                )

        subsession_headers = [
            (pretty_name(key), len(list(group)))
            for key, group in
            itertools.groupby(column_name_tuples, key=lambda x: x[0])
            ]

        model_headers = [
            (pretty_name(key[1]), len(list(group)))
            for key, group in
            itertools.groupby(column_name_tuples, key=lambda x: (x[0], x[1]))
            ]

        field_headers = [
            pretty_name(key[2]) for key, group in
            itertools.groupby(column_name_tuples, key=lambda x: x)
            ]

        # dictionary for json response
        # will be used only if json request  is done
        self.context_json = []
        for i, row in enumerate(rows):
            d_row = OrderedDict()
            d_row['participant_label'] = participant_labels[i]
            for t, v in zip(column_name_tuples, row):
                d_row['.'.join(t)] = v
            self.context_json.append(d_row)

        context = super(SessionResults, self).get_context_data(**kwargs)
        context.update({
            'subsession_headers': subsession_headers,
            'model_headers': model_headers,
            'field_headers': field_headers,
            'rows': rows})
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.META.get('CONTENT_TYPE') == 'application/json':
            return JsonResponse(self.context_json, safe=False)
        else:
            return self.render_to_response(context)


class SessionDescription(AdminSessionPageMixin, vanilla.TemplateView):

    def get_context_data(self, **kwargs):
        context = super(SessionDescription, self).get_context_data(**kwargs)
        config_obj = SessionConfig(self.session.config)
        context.update(config_obj.get_info())
        return context


class Sessions(vanilla.ListView):
    template_name = 'otree/admin/Sessions.html'

    url_pattern = r"^sessions/(?P<archive>archive)?$"

    def get_context_data(self, **kwargs):
        context = super(Sessions, self).get_context_data(**kwargs)
        context.update({
            'is_debug': settings.DEBUG,
        })
        return context

    def get_queryset(self):
        return Session.objects.filter(
            is_demo=False).order_by('archived', '-pk')


class ServerCheck(vanilla.TemplateView):
    template_name = 'otree/admin/ServerCheck.html'

    url_pattern = r"^server_check/$"

    def app_is_on_heroku(self):
        return 'heroku' in self.request.get_host()

    def get_context_data(self, **kwargs):
        sqlite = settings.DATABASES['default']['ENGINE'].endswith('sqlite3')
        debug = settings.DEBUG
        regular_sentry = hasattr(settings, 'RAVEN_CONFIG')
        heroku_sentry = os.environ.get('SENTRY_DSN')
        sentry = regular_sentry or heroku_sentry
        auth_level = settings.AUTH_LEVEL in {'DEMO', 'STUDY'}
        heroku = self.app_is_on_heroku()
        runserver = 'runserver' in sys.argv
        db_synced = db_status_ok()
        pypi_results = check_pypi_for_updates()

        return {
            'sqlite': sqlite,
            'debug': debug,
            'sentry': sentry,
            'auth_level': auth_level,
            'heroku': heroku,
            'runserver': runserver,
            'db_synced': db_synced,
            'pypi_results': pypi_results
        }


class OtreeCoreUpdateCheck(vanilla.View):

    url_pattern = r"^version_cached/$"

    # cached per process
    results = None

    def get(self, request, *args, **kwargs):
        if OtreeCoreUpdateCheck.results is None:
            OtreeCoreUpdateCheck.results = check_pypi_for_updates()
        return JsonResponse(OtreeCoreUpdateCheck.results, safe=True)


class CreateBrowserBotsSession(vanilla.View):

    url_pattern = r"^create_browser_bots_session/$"

    def get(self, request, *args, **kwargs):
        # return browser bots check
        sqlite = settings.DATABASES['default']['ENGINE'].endswith('sqlite3')

        return JsonResponse({
            'sqlite': sqlite,
            'runserver': 'runserver' in sys.argv
        })

    def post(self, request, *args, **kwargs):
        num_participants = int(request.POST['num_participants'])
        session_config_name = request.POST['session_config_name']
        bot_case_number = int(request.POST['bot_case_number'])
        session = create_session(
            session_config_name=session_config_name,
            num_participants=num_participants,
            bot_case_number=bot_case_number,
            force_browser_bots=True
        )
        BrowserBotsLauncherSessionCode.objects.update_or_create(
            # i don't know why the update_or_create arg is called 'defaults'
            # because it will update even if the instance already exists
            # maybe for consistency with get_or_create
            defaults={'code': session.code}
        )
        channels.Group('browser_bot_wait').send(
            {'text': json.dumps({'status': 'session_ready'})}
        )

        return HttpResponse(session.code)


class CloseBrowserBotsSession(vanilla.View):

    url_pattern = r"^close_browser_bots_session/$"

    def post(self, request, *args, **kwargs):
        BrowserBotsLauncherSessionCode.objects.all().delete()
        return HttpResponse('ok')
