import json
import logging
import django.db
import django.utils.timezone
import traceback
import time
from channels.generic.websocket import (
    JsonWebsocketConsumer, WebsocketConsumer)
from django.core.signing import Signer, BadSignature
import otree.session
from otree.channels.utils import get_chat_group
from otree.models import Participant, Session
from otree.models_concrete import (
    CompletedGroupWaitPage, CompletedSubsessionWaitPage, ChatMessage)
from otree.common_internal import (
    get_models_module
)
import otree.channels.utils as channel_utils
from otree.models_concrete import (
    ParticipantRoomVisit,
    BrowserBotsLauncherSessionCode)
from otree.room import ROOM_DICT
import otree.bots.browser
from otree.export import export_wide, export_app
import io
import base64
import datetime
from django.conf import settings
from django.shortcuts import reverse
from otree.views.admin import CreateSessionForm
from otree.session import SESSION_CONFIGS_DICT

logger = logging.getLogger(__name__)

ALWAYS_UNRESTRICTED = 'ALWAYS_UNRESTRICTED'
UNRESTRICTED_IN_DEMO_MODE = 'UNRESTRICTED_IN_DEMO_MODE'


class InvalidWebSocketParams(Exception):
    '''exception to raise when websocket params are invalid'''


class _OTreeJsonWebsocketConsumer(JsonWebsocketConsumer):
    """
    This is not public API, might change at any time.
    """

    def clean_kwargs(self, **kwargs):
        '''
        subclasses should override if the route receives a comma-separated params arg.
        otherwise, this just passes the route kwargs as is (usually there is just one).
        The output of this method is passed to self.group_name(), self.post_connect,
        and self.pre_disconnect, so within each class, all 3 of those methods must
        accept the same args (or at least take a **kwargs wildcard, if the args aren't used)
        '''
        return kwargs

    def group_name(self, **kwargs):
        raise NotImplementedError()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleaned_kwargs = self.clean_kwargs(**self.scope['url_route']['kwargs'])
        group_name = self.group_name(**self.cleaned_kwargs)
        self.groups = [group_name] if group_name else []

    unrestricted_when = ''

    # there is no login_required for channels
    # so we need to make our own
    # https://github.com/django/channels/issues/1241
    def connect(self):

        AUTH_LEVEL = settings.AUTH_LEVEL

        auth_required = (
            (not self.unrestricted_when) and AUTH_LEVEL
            or
            self.unrestricted_when == UNRESTRICTED_IN_DEMO_MODE and AUTH_LEVEL == 'STUDY'
        )

        if auth_required and not self.scope['user'].is_staff:
            msg = 'rejected un-authenticated access to websocket path {}'.format(self.scope['path'])
            logger.warning(msg)
            # consider also self.accept() then send error message then self.close(code=1008)
            # this only affects otree core websockets.
        else:
            # need to accept no matter what, so we can at least send
            # an error message
            self.accept()
            self.post_connect(**self.cleaned_kwargs)

    def post_connect(self, **kwargs):
        pass

    def disconnect(self, message, **kwargs):
        self.pre_disconnect(**self.cleaned_kwargs)

    def pre_disconnect(self, **kwargs):
        pass

    def receive_json(self, content, **etc):
        self.post_receive_json(content, **self.cleaned_kwargs)

    def post_receive_json(self, content, **kwargs):
        pass


class GroupByArrivalTime(_OTreeJsonWebsocketConsumer):

    unrestricted_when = ALWAYS_UNRESTRICTED

    def clean_kwargs(self, params):
        session_pk, page_index, app_name, player_id = params.split(',')
        return {
            'app_name': app_name,
            'session_pk': int(session_pk),
            'page_index': int(page_index),
            'player_id': int(player_id)
        }

    def group_name(self, app_name, player_id, page_index, session_pk):
        gn = channel_utils.gbat_group_name(
            session_pk, page_index)
        return gn

    def post_connect(self, app_name, player_id, page_index, session_pk):
        models_module = get_models_module(app_name)
        group_id_in_subsession = models_module.Group.objects.filter(
            player__id=player_id).values_list(
            'id_in_subsession', flat=True)[0]

        ready = CompletedGroupWaitPage.objects.filter(
            page_index=page_index,
            id_in_subsession=int(group_id_in_subsession),
            session_id=session_pk,
        ).exists()
        if ready:
            self.gbat_ready()

    def gbat_ready(self, event=None):
        self.send_json({'status': 'ready'})


class WaitPage(_OTreeJsonWebsocketConsumer):

    unrestricted_when = ALWAYS_UNRESTRICTED

    def clean_kwargs(self, params):
        session_pk, page_index, group_id_in_subsession = params.split(',')
        return {
            'session_pk': int(session_pk),
            'page_index': int(page_index),
            # don't convert group_id_in_subsession to int yet, it might be null
            'group_id_in_subsession': group_id_in_subsession,
        }

    def group_name(self, session_pk, page_index, group_id_in_subsession):
        return channel_utils.wait_page_group_name(
            session_pk, page_index, group_id_in_subsession)

    def post_connect(self, session_pk, page_index, group_id_in_subsession):
        # in case message was sent before this web socket connects
        if group_id_in_subsession:
            ready = CompletedGroupWaitPage.objects.filter(
                page_index=page_index,
                id_in_subsession=int(group_id_in_subsession),
                session_id=session_pk,
            ).exists()
        else:  # subsession
            ready = CompletedSubsessionWaitPage.objects.filter(
                page_index=page_index,
                session_id=session_pk,
            ).exists()
        if ready:
            self.wait_page_ready()

    def wait_page_ready(self, event=None):
        self.send_json({'status': 'ready'})


class DetectAutoAdvance(_OTreeJsonWebsocketConsumer):

    unrestricted_when = ALWAYS_UNRESTRICTED

    def clean_kwargs(self, params):
        participant_code, page_index = params.split(',')
        return {
            'participant_code': participant_code,
            'page_index': int(page_index),
        }

    def group_name(self, page_index, participant_code):
        return channel_utils.auto_advance_group(participant_code)

    def post_connect(self, page_index, participant_code):
        # in case message was sent before this web socket connects
        result = Participant.objects.filter(
            code=participant_code).values_list(
            '_index_in_pages', flat=True)
        try:
            page_should_be_on = result[0]
        except IndexError:
            # doesn't get shown because not yet localized
            self.send_json({'error': 'Participant not found in database.'})
            return
        if page_should_be_on > page_index:
            self.auto_advanced()

    def auto_advanced(self, event=None):
        self.send_json({'auto_advanced': True})


class BaseCreateSession(_OTreeJsonWebsocketConsumer):

    def group_name(self, **kwargs):
        return None

    def send_response_to_browser(self, event: dict):
        raise NotImplemented

    def create_session_then_send_start_link(self, use_browser_bots, **session_kwargs):
        try:
            session = otree.session.create_session(**session_kwargs)
            if use_browser_bots:
                otree.bots.browser.initialize_session(
                    session_pk=session.pk,
                    case_number=None
                )
            session.save()
        except Exception as e:

            # full error message is printed to console (though sometimes not?)
            error_message = 'Failed to create session: "{}"'.format(e)
            traceback_str = traceback.format_exc()
            self.send_response_to_browser(dict(
                error=error_message,
                traceback=traceback_str,
            ))
            raise

        session_home_view = 'MTurkCreateHIT' if session.is_mturk() else 'SessionStartLinks'

        self.send_response_to_browser(
            {'session_url': reverse(session_home_view, args=[session.code])}
        )


class CreateDemoSession(BaseCreateSession):

    unrestricted_when = UNRESTRICTED_IN_DEMO_MODE

    def send_response_to_browser(self, event: dict):
        self.send_json(event)

    def post_receive_json(self, form_data: dict):
        session_config_name = form_data['session_config']
        config = SESSION_CONFIGS_DICT.get(session_config_name)
        if not config:
            msg = f'Session config "{session_config_name}" does not exist.'
            self.send_json(
                {'validation_errors': msg})
            return

        num_participants = config['num_demo_participants']
        use_browser_bots = config.get('use_browser_bots', False)

        self.create_session_then_send_start_link(
            session_config_name=session_config_name,
            use_browser_bots=use_browser_bots,
            num_participants=num_participants,
            is_demo=True
        )


class CreateSession(BaseCreateSession):

    unrestricted_when = None

    def group_name(self, **kwargs):
        return 'create_session'

    def post_receive_json(self, form_data: dict):
        form = CreateSessionForm(data=form_data)
        if not form.is_valid():
            self.send_json({'validation_errors': form.errors})
            return

        session_config_name = form.cleaned_data['session_config']
        is_mturk = form.cleaned_data['is_mturk']

        config = SESSION_CONFIGS_DICT[session_config_name]

        num_participants = form.cleaned_data['num_participants']
        if is_mturk:
            num_participants *= settings.MTURK_NUM_PARTICIPANTS_MULTIPLE

        edited_session_config_fields = {}

        for field in config.editable_fields():
            html_field_name = config.html_field_name(field)
            old_value = config[field]

            # to allow concise unit tests, we can simply omit any fields we don't
            # want to change. this allows us to write more concise
            # unit tests.
            # EXCEPT for boolean fields -- omitting
            # it means we turn it off.
            # ideally we could interpret omitted boolean fields as unchanged
            # and False as unchecked, but HTML & serializeArray omits
            # unchecked checkboxes from form data.

            if isinstance(old_value, bool):
                new_value = bool(form_data.get(html_field_name))
                if old_value != new_value:
                    edited_session_config_fields[field] = new_value
            else:
                new_value_raw = form_data.get(html_field_name, '')
                if new_value_raw != '':
                    # don't use isinstance because that will catch bool also
                    if type(old_value) is int:
                        # in case someone enters 1.0 instead of 1
                        new_value = int(float(new_value_raw))
                    else:
                        new_value = type(old_value)(new_value_raw)
                    if old_value != new_value:
                        edited_session_config_fields[field] = new_value

        use_browser_bots = edited_session_config_fields.get(
            'use_browser_bots',
            config.get('use_browser_bots', False)
        )

        # if room_name is missing, it will be empty string
        room_name = form.cleaned_data['room_name'] or None

        self.create_session_then_send_start_link(
            session_config_name=session_config_name,
            num_participants=num_participants,
            is_demo=False,
            is_mturk=is_mturk,
            edited_session_config_fields=edited_session_config_fields,
            use_browser_bots=use_browser_bots,
            room_name=room_name,
        )

        if room_name:
            channel_utils.sync_group_send_wrapper(
                type='room_session_ready',
                group=channel_utils.room_participants_group_name(room_name),
                event={}
            )

    def send_response_to_browser(self, event: dict):
        '''
        Send to a group instead of the channel only,
        because if the websocket disconnects during creation of a large session,
        (due to temporary network error, etc, or Heroku H15, 55 seconds without ping)
        the user could be stuck on "please wait" forever.
        the downside is that if two admins create sessions around the same time,
        your page could automatically redirect to the other admin's session.
        '''
        [group] = self.groups
        channel_utils.sync_group_send_wrapper(
            type='session_created',
            group=group,
            event=event
        )

    def session_created(self, event):
        self.send_json(event)


class RoomAdmin(_OTreeJsonWebsocketConsumer):

    unrestricted_when = None

    def group_name(self, room):
        return channel_utils.room_admin_group_name(room)

    def post_connect(self, room):
        room_object = ROOM_DICT[room]

        now = time.time()
        stale_threshold = now - 15
        present_list = ParticipantRoomVisit.objects.filter(
            room_name=room_object.name,
            last_updated__gte=stale_threshold,
        ).values_list('participant_label', flat=True)

        # make it JSON serializable
        present_list = list(present_list)

        self.send_json({
            'status': 'load_participant_lists',
            'participants_present': present_list,
        })

        # prune very old visits -- don't want a resource leak
        # because sometimes not getting deleted on WebSocket disconnect
        very_stale_threshold = now - 10 * 60
        ParticipantRoomVisit.objects.filter(
            room_name=room_object.name,
            last_updated__lt=very_stale_threshold,
        ).delete()

    def roomadmin_update(self, event):
        del event['type']
        self.send_json(event)


class RoomParticipant(_OTreeJsonWebsocketConsumer):

    unrestricted_when = ALWAYS_UNRESTRICTED

    def clean_kwargs(self, params):
        room_name, participant_label, tab_unique_id = params.split(',')
        return {
            'room_name': room_name,
            'participant_label': participant_label,
            'tab_unique_id': tab_unique_id,
        }

    def group_name(self, room_name, participant_label, tab_unique_id):
        return channel_utils.room_participants_group_name(room_name)

    def post_connect(self, room_name, participant_label, tab_unique_id):
        if room_name in ROOM_DICT:
            room = ROOM_DICT[room_name]
        else:
            # doesn't get shown because not yet localized
            self.send_json({'error': 'Invalid room name "{}".'.format(room_name)})
            return
        if room.has_session():
            self.room_session_ready()
        else:
            try:
                ParticipantRoomVisit.objects.create(
                    participant_label=participant_label,
                    room_name=room_name,
                    tab_unique_id=tab_unique_id,
                    last_updated=time.time(),
                )
            except django.db.IntegrityError:
                # possible that the tab connected twice
                # without disconnecting in between
                # because of WebSocket failure
                # tab_unique_id is unique=True,
                # so this will throw an integrity error.
                # 2017-09-17: I saw the integrityerror on macOS.
                # previously, we logged this, but i see no need to do that.
                pass
            channel_utils.sync_group_send_wrapper(
                type='roomadmin.update',
                group=channel_utils.room_admin_group_name(room_name),
                event={
                    'status': 'add_participant',
                    'participant': participant_label
                }
            )

    def pre_disconnect(self, room_name, participant_label, tab_unique_id):
        if room_name in ROOM_DICT:
            room = ROOM_DICT[room_name]
        else:
            # doesn't get shown because not yet localized
            self.send_json({'error': 'Invalid room name "{}".'.format(room_name)})
            return

        # should use filter instead of get,
        # because if the DB is recreated,
        # the record could already be deleted
        ParticipantRoomVisit.objects.filter(
            participant_label=participant_label,
            room_name=room_name,
            tab_unique_id=tab_unique_id).delete()

        event = {
            'status': 'remove_participant',
        }
        if room.has_participant_labels():
            if ParticipantRoomVisit.objects.filter(
                    participant_label=participant_label,
                    room_name=room_name
            ).exists():
                return
            # it's ok if there is a race condition --
            # in JS removing a participant is idempotent
            event['participant'] = participant_label
        admin_group = channel_utils.room_admin_group_name(room_name)
        channel_utils.sync_group_send_wrapper(group=admin_group, type='roomadmin_update', event=event)

    def room_session_ready(self, event=None):
        self.send_json({'status': 'session_ready'})


class BrowserBotsLauncher(_OTreeJsonWebsocketConsumer):

    # OK to be unrestricted because this websocket doesn't create the session,
    # or do anything sensitive.
    unrestricted_when = ALWAYS_UNRESTRICTED

    def group_name(self, session_code):
        return channel_utils.browser_bots_launcher_group(session_code)

    def send_completion_message(self, event):
        # don't need to put in JSON since it's just a participant code
        self.send(event['text'])


class BrowserBot(_OTreeJsonWebsocketConsumer):

    unrestricted_when = ALWAYS_UNRESTRICTED

    def group_name(self):
        return 'browser_bot_wait'

    def post_connect(self):
        launcher_session_info = BrowserBotsLauncherSessionCode.objects.first()
        if launcher_session_info:
            self.browserbot_sessionready()

    def browserbot_sessionready(self, event=None):
        self.send_json({'status': 'session_ready'})

class ChatConsumer(_OTreeJsonWebsocketConsumer):

    unrestricted_when = ALWAYS_UNRESTRICTED

    def clean_kwargs(self, params):

        signer = Signer(sep='/')
        try:
            original_params = signer.unsign(params)
        except BadSignature:
            raise InvalidWebSocketParams

        channel, participant_id = original_params.split('/')

        return {
            'channel': channel,
            'participant_id': int(participant_id),
        }

    def group_name(self, channel, participant_id):
        return get_chat_group(channel)

    def post_connect(self, channel, participant_id):

        history = ChatMessage.objects.filter(
            channel=channel).order_by('timestamp').values(
            'nickname', 'body', 'participant_id'
        )

        # Convert ValuesQuerySet to list
        # but is it ok to send a list (not a dict) as json?
        self.send_json(list(history))

    def post_receive_json(self, content, channel, participant_id):
        # in the Channels docs, the example has a separate msg_consumer
        # channel, so this can be done asynchronously.
        # but i think the perf is probably good enough.
        # moving into here for simplicity, especially for testing.
        nickname_signed = content['nickname_signed']
        nickname = Signer().unsign(nickname_signed)
        body = content['body']

        chat_message = dict(
            nickname=nickname,
            body=body,
            participant_id=participant_id
        )

        [group] = self.groups
        channel_utils.sync_group_send_wrapper(
            type='chat_sendmessages', group=group, event={'chats': [chat_message]}
        )

        ChatMessage.objects.create(
            participant_id=participant_id,
            channel=channel,
            body=body,
            nickname=nickname
        )


    def chat_sendmessages(self, event):
        chats = event['chats']
        self.send_json(chats)


class ExportData(_OTreeJsonWebsocketConsumer):

    '''
    I load tested this locally with sqlite/redis and:
    - large files up to 22MB (by putting long text in LongStringFields)
    - thousands of participants/rounds, 111000 rows and 20 cols in excel file.
    '''

    unrestricted_when = None

    def post_receive_json(self, content: dict):
        '''
        if an app name is given, export the app.
        otherwise, export all the data (wide).
        don't need time_spent or chat yet, they are quick enough
        '''

        file_extension = content['file_extension']
        app_name = content.get('app_name')

        if file_extension == 'xlsx':
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            IOClass = io.BytesIO
        else:
            mime_type = 'text/csv'
            IOClass = io.StringIO

        iso_date = datetime.date.today().isoformat()
        with IOClass() as fp:
            if app_name:
                export_app(app_name, fp, file_extension=file_extension)
                file_name_prefix = app_name
            else:
                export_wide(fp, file_extension=file_extension)
                file_name_prefix = 'all_apps_wide'
            data = fp.getvalue()

        file_name = '{}_{}.{}'.format(
            file_name_prefix, iso_date, file_extension)

        if file_extension == 'xlsx':
            data = base64.b64encode(data).decode('utf-8')

        content.update(
            file_name=file_name,
            data=data,
            mime_type=mime_type
        )
        # this doesn't go through channel layer, so it is probably safer
        # in terms of sending large data

        self.send_json(content)

    def group_name(self, **kwargs):
        return None


class NoOp(WebsocketConsumer):
    pass


class LifespanApp:
    '''
    temporary shim for https://github.com/django/channels/issues/1216
    needed so that hypercorn doesn't display an error.
    this uses ASGI 2.0 format, not the newer 3.0 single callable
    '''

    def __init__(self, scope):
        self.scope = scope

    async def __call__(self, receive, send):
        if self.scope['type'] == 'lifespan':
            while True:
                message = await receive()
                if message['type'] == 'lifespan.startup':
                    await send({'type': 'lifespan.startup.complete'})
                elif message['type'] == 'lifespan.shutdown':
                    await send({'type': 'lifespan.shutdown.complete'})
                    return
