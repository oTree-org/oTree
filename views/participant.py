import threading
import time

import django.utils.timezone
import otree.common_internal
import otree.constants_internal as constants
import otree.models
import otree.views.admin
import otree.views.mturk
import vanilla
from django.urls import reverse
from django.http import (
    HttpResponse, HttpResponseRedirect,
    HttpResponseNotFound
)
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from otree.common_internal import (
    make_hash, add_params_to_url, get_redis_conn
)
import otree.channels.utils as channel_utils
from otree.models import Participant, Session
from otree.models_concrete import (
    ParticipantRoomVisit, BrowserBotsLauncherSessionCode)
from otree.room import ROOM_DICT
from otree.views.abstract import (
    GenericWaitPageMixin,
    get_redis_lock, NO_PARTICIPANTS_LEFT_MSG)


start_link_thread_lock = threading.RLock()

class OutOfRangeNotification(vanilla.View):
    name_in_url = 'shared'

    def dispatch(self, request):
        return TemplateResponse(
            request, 'otree/OutOfRangeNotification.html'
        )

    url_pattern = '^OutOfRangeNotification/$'


class InitializeParticipant(vanilla.UpdateView):

    url_pattern = r'^InitializeParticipant/(?P<participant_code>[a-z0-9]+)/$'

    def get(self, request, participant_code):

        participant = get_object_or_404(
            Participant,
            code=participant_code
        )

        if participant._index_in_pages == 0:
            participant._index_in_pages = 1
            participant.visited = True

            # participant.label might already have been set
            participant.label = participant.label or self.request.GET.get(
                constants.participant_label
            )
            participant.ip_address = self.request.META['REMOTE_ADDR']

            now = django.utils.timezone.now()
            participant.time_started = now
            participant._last_page_timestamp = time.time()

            participant.save()
        first_url = participant._url_i_should_be_on()
        return HttpResponseRedirect(first_url)


class MTurkLandingPage(vanilla.TemplateView):

    def get_template_names(self):
        hit_settings = self.session.config['mturk_hit_settings']
        return [hit_settings['preview_template']]

    url_pattern = r"^MTurkLandingPage/(?P<session_code>[a-z0-9]+)/$"

    def dispatch(self, request, session_code):
        self.session = get_object_or_404(
            otree.models.Session, code=session_code
        )
        return super().dispatch(request)

    def get_context_data(self):
        '''
        hack for compatibility because the project template's
        MTurkPreview.html inherits from Page.html which uses all these
        nonexistent template vars. Should change that.
        '''
        return {
            'view': {
                'remaining_timeout_seconds': None,
                'socket_url': '',
                'redirect_url': '',
            },
            'form': {'errors': None, 'non_field_errors': None},
            'participant': {'is_browser_bot': False}
        }

    def get(self, request):
        assignment_id = self.request.GET.get('assignmentId')
        if assignment_id and assignment_id != 'ASSIGNMENT_ID_NOT_AVAILABLE':
            url_start = reverse('MTurkStart', args=(self.session.code,))
            url_start = add_params_to_url(url_start, {
                'assignmentId': self.request.GET['assignmentId'],
                'workerId': self.request.GET['workerId']})
            return HttpResponseRedirect(url_start)

        context = self.get_context_data()
        return self.render_to_response(context)


class MTurkStart(vanilla.View):

    url_pattern = r"^MTurkStart/(?P<session_code>[a-z0-9]+)/$"

    def dispatch(self, request, session_code):
        self.session = get_object_or_404(
            otree.models.Session, code=session_code
        )
        return super().dispatch(request)

    def get(self, request):
        assignment_id = self.request.GET['assignmentId']
        worker_id = self.request.GET['workerId']
        qualification_id = self.session.config['mturk_hit_settings'].get('grant_qualification_id')
        use_sandbox=self.session.mturk_use_sandbox
        if qualification_id and not use_sandbox:
            # if using sandbox, there is no point in granting quals.
            # https://groups.google.com/forum/#!topic/otree/aAmqTUF-b60

            # don't pass request arg, because we don't want to show a message.
            # using the fully qualified name because that seems to make mock.patch work
            mturk_client = otree.views.mturk.get_mturk_client(
                use_sandbox=use_sandbox)
            # seems OK to assign this multiple times
            mturk_client.associate_qualification_with_worker(
                QualificationTypeId=qualification_id,
                WorkerId=worker_id,
                # Mturk complains if I omit IntegerValue
                IntegerValue=1
            )
        try:
            # just check if this worker already game, but
            # don't filter for assignment, because maybe they already started
            # and returned the previous assignment
            # in this case, we should assign back to the same participant
            # so that we don't get duplicates in the DB, and so people
            # can't snoop and try the HIT first, then re-try to get a bigger bonus
            participant = self.session.participant_set.get(
                mturk_worker_id=worker_id)
        except Participant.DoesNotExist:
            with get_redis_lock(name='start_links') or start_link_thread_lock:
                try:
                    participant = self.session.participant_set.filter(
                        visited=False
                    ).order_by('id')[0]
                except IndexError:
                    return HttpResponseNotFound(NO_PARTICIPANTS_LEFT_MSG)

                # 2014-10-17: needs to be here even if it's also set in
                # the next view to prevent race conditions
                # this needs to be inside the lock
                participant.visited = True
                participant.mturk_worker_id = worker_id
        # reassign assignment_id, even if they are returning, because maybe they accepted
        # and then returned, then re-accepted with a different assignment ID
        # if it's their second time
        participant.mturk_assignment_id = assignment_id
        participant.save()
        return HttpResponseRedirect(participant._start_url())


def get_existing_or_new_participant(session, label):
    if label:
        try:
            return session.participant_set.get(label=label)
        except Participant.DoesNotExist:
            pass
    return session.participant_set.filter(
        visited=False).order_by('id').first()


def get_participant_with_cookie_check(session, cookies):
    cookie_name = 'session_{}_participant'.format(session.code)
    participant_code = cookies.get(cookie_name)
    # this could return None
    if participant_code:
        return Participant.objects.filter(code=participant_code).first()
    participant = session.participant_set.filter(
        visited=False).order_by('id').first()
    if participant:
        cookies[cookie_name] = participant.code
        return participant


def participant_start_page_or_404(session, *, label, cookies=None):
    '''pass request.session as an arg if you want to get/set a cookie'''
    with get_redis_lock(name='start_links') or start_link_thread_lock:
        if cookies is None:
            participant = get_existing_or_new_participant(session, label)
        else:
            participant = get_participant_with_cookie_check(session, cookies)
        if not participant:
            return HttpResponseNotFound(NO_PARTICIPANTS_LEFT_MSG)

        # needs to be here even if it's also set in
        # the next view to prevent race conditions
        participant.visited = True
        if label:
            participant.label = label
        participant.save()

    return HttpResponseRedirect(participant._start_url())


class JoinSessionAnonymously(vanilla.View):

    url_pattern = r'^join/(?P<anonymous_code>[a-z0-9]+)/$'

    def get(self, request, anonymous_code):
        session = get_object_or_404(
            otree.models.Session, _anonymous_code=anonymous_code
        )
        label = self.request.GET.get('participant_label')
        return participant_start_page_or_404(session, label=label)


class AssignVisitorToRoom(GenericWaitPageMixin, vanilla.View):

    url_pattern = r'^room/(?P<room>\w+)/$'

    def dispatch(self, request, room):
        self.room_name = room
        try:
            room = ROOM_DICT[self.room_name]
        except KeyError:
            return HttpResponseNotFound('Invalid room specified in url')

        label = self.request.GET.get(
            'participant_label', ''
        )

        if room.has_participant_labels():
            if label:
                missing_label = False
                invalid_label = label not in room.get_participant_labels()
            else:
                missing_label = True
                invalid_label = False

            # needs to be easy to re-enter label, in case we are in kiosk
            # mode
            if missing_label or invalid_label and not room.use_secure_urls:
                return render(request,
                    "otree/RoomInputLabel.html",
                    {'invalid_label': invalid_label}
                )

            if room.use_secure_urls:
                hash = self.request.GET.get('hash')
                if hash != make_hash(label):
                    return HttpResponseNotFound(
                        'Invalid hash parameter. use_secure_urls is True, '
                        'so you must use the participant-specific URL.'
                    )

        session = room.get_session()
        if session is None:
            self.tab_unique_id = otree.common_internal.random_chars_10()
            self._socket_url = channel_utils.room_participant_path(
                self.room_name,
                label,
                # random chars in case the participant has multiple tabs open
                self.tab_unique_id
            )
            return render(request,
                "otree/WaitPageRoom.html",
                {
                    'view': self, 'title_text': _('Please wait'),
                    'body_text': _('Waiting for your session to begin')
                }
            )

        if label:
            cookies = None
        else:
            cookies = request.session


        # 2017-08-02: changing the behavior so that even in a room without
        # participant_label_file, 2 requests for the same start URL with same label
        # will return the same participant. Not sure if the previous behavior
        # (assigning to 2 different participants) was intentional or bug.
        return participant_start_page_or_404(session, label=label, cookies=cookies)

    def get_context_data(self, **kwargs):
        return {
            'room': self.room_name,
        }

    def socket_url(self):
        return self._socket_url

    def redirect_url(self):
        return self.request.get_full_path()


class ParticipantRoomHeartbeat(vanilla.View):

    url_pattern = r'^ParticipantRoomHeartbeat/(?P<tab_unique_id>\w+)/$'

    def get(self, request, tab_unique_id):
        # better not to return 404, because in practice, on Firefox,
        # this was still being requested after the session started.
        ParticipantRoomVisit.objects.filter(
            tab_unique_id=tab_unique_id
        ).update(last_updated=time.time())
        return HttpResponse('')


class ParticipantHeartbeatGBAT(vanilla.View):
    url_pattern = r'^ParticipantHeartbeatGBAT/(?P<participant_code>\w+)/$'

    def get(self, request, participant_code):
        Participant.objects.filter(code=participant_code).update(
            _last_request_timestamp=time.time())
        return HttpResponse('')


class BrowserBotStartLink(GenericWaitPageMixin, vanilla.View):
    '''should i move this to another module?
    because the rest of these views are accessible without password login.
    '''

    url_pattern = r'^browser_bot_start/$'

    def dispatch(self, request):
        get_redis_conn() # why do we do this?
        session_info = BrowserBotsLauncherSessionCode.objects.first()
        if session_info:
            session = Session.objects.get(code=session_info.code)
            with get_redis_lock(name='start_links') or start_link_thread_lock:
                participant = session.participant_set.filter(
                    visited=False).order_by('id').first()
                if not participant:
                    return HttpResponseNotFound(NO_PARTICIPANTS_LEFT_MSG)

                # 2014-10-17: needs to be here even if it's also set in
                # the next view to prevent race conditions
                participant.visited = True
                participant.save()

            return HttpResponseRedirect(participant._start_url())
        else:
            ctx = {'view': self, 'title_text': 'Please wait',
                   'body_text': 'Waiting for browser bots session to begin'}
            return render(request, "otree/WaitPage.html", ctx)

    def socket_url(self):
        return '/browser_bot_wait/'

    def redirect_url(self):
        return self.request.get_full_path()


