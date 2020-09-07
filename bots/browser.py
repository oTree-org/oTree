from typing import Dict
import json
import threading
import logging
from collections import OrderedDict

import channels
import otree.channels.utils as channel_utils
import traceback

import otree.common_internal
from otree import common_internal

from otree.common_internal import get_redis_conn

from .runner import make_bots
from .bot import ParticipantBot
import random

from otree.models import Session
from channels.layers import get_channel_layer


REDIS_KEY_PREFIX = 'otree-bots'

# if you are testing all configs from the CLI browser bot launcher,
# and each app has multiple cases, it's possible to end up with many
# bots in the history.
# usually this wouldn't matter,
# but timeoutworker may try to load the pages after they have been completed
# (it will POST then get redirected to GET)
SESSIONS_PRUNE_LIMIT = 80

# global variable that holds the browser bot worker instance in memory
browser_bot_worker = None  # type: Worker

# these locks are only necessary when using runserver
# because then the botworker stuff is done by one of the 4 worker threads.
prepare_submit_lock = threading.Lock()
add_or_remove_bot_lock = threading.Lock()

logger = logging.getLogger('otree.test.browser_bots')


class BotRequestError(Exception):
    '''
    if USE_REDIS==True, this exception will be converted to a dict
    and passed through Redis.
    if USE_REDIS==False, this will raise normally.
    '''
    pass


PARTICIPANT_NOT_IN_BOTWORKER_MSG = (
    "Participant {participant_code} not loaded in botworker. "
    "This can happen for several reasons: "
    "(1) You are running multiple botworkers "
    "(2) You restarted the botworker after creating the session "
    "(3) The bots expired "
    "(the botworker stores bots for "
    "only the most recent {prune_limit} sessions)."
)


class Worker:
    def __init__(self, redis_conn=None):
        self.redis_conn = redis_conn
        self.participants_by_session = OrderedDict()
        self.browser_bots = {} # type: Dict[str, ParticipantBot]

    def initialize_session(self, session_pk, case_number):
        self.prune()
        self.participants_by_session[session_pk] = []

        session = Session.objects.get(pk=session_pk)
        if case_number is None:
            # choose one randomly
            from otree.session import SessionConfig
            config = SessionConfig(session.config)
            num_cases = config.get_num_bot_cases()
            case_number = random.choice(range(num_cases))

        bots = make_bots(
            session_pk=session_pk, case_number=case_number, use_browser_bots=True
        )
        for bot in bots:
            self.participants_by_session[session_pk].append(
                bot.participant_code)
            self.browser_bots[bot.participant_code] = bot

    def prune(self):
        '''to avoid memory leaks'''
        with add_or_remove_bot_lock:
            if len(self.participants_by_session) > SESSIONS_PRUNE_LIMIT:
                _, p_codes = self.participants_by_session.popitem(last=False)
                for participant_code in p_codes:
                    self.browser_bots.pop(participant_code, None)

    def get_bot(self, participant_code):
        try:
            return self.browser_bots[participant_code]
        except KeyError:
            msg = PARTICIPANT_NOT_IN_BOTWORKER_MSG.format(
                participant_code=participant_code, prune_limit=SESSIONS_PRUNE_LIMIT)
            raise BotRequestError(msg)

    def get_next_post_data(self, participant_code):
        bot = self.get_bot(participant_code)
        try:
            submission = next(bot.submits_generator)
        except StopIteration:
            # don't prune it because can cause flakiness if
            # there are other GET requests coming in. it will be pruned
            # when new sessions are created anyway.

            # return None instead of raising an exception, because
            # None can easily be serialized in Redis. Means the code can be
            # basically the same for Redis and non-Redis
            return None
        else:
            # because we are returning it through Redis, need to pop it
            # here
            submission.pop('page_class')
            return submission['post_data']

    def set_attributes(self, participant_code, request_path, html):
        bot = self.get_bot(participant_code)
        # so that any asserts in the PlayerBot work.
        bot.path = request_path
        bot.html = html

    def ping(self, *args, **kwargs):
        pass

    def redis_listen(self):
        print('botworker is listening for messages through Redis')
        while True:
            self.try_process_one_redis_message()

    def try_process_one_redis_message(self):
        '''break it out into a separate method for testing purposes'''

        # blpop returns a tuple
        result = None

        # put it in a loop so that we can still receive KeyboardInterrupts
        # otherwise it will block
        while result is None:
            result = self.redis_conn.blpop(REDIS_KEY_PREFIX, timeout=3)

        key, message_bytes = result
        message = json.loads(message_bytes.decode('utf-8'))
        response_key = message['response_key']
        kwargs = message['kwargs']
        method = getattr(self, message['method'])

        try:
            retval = method(**kwargs)
            response = {'retval': retval}
        except BotRequestError as exc:
            # request error means the request received through Redis
            # was invalid.
            # use str instead of repr here
            response = {'error': str(exc)}
        except Exception as exc:
            # un-anticipated error
            response = {
                'error': repr(exc),
                'traceback': traceback.format_exc()
            }
            # don't raise, because then this would crash.
            # logger.exception() will record the full traceback
            logger.exception(repr(exc))
        finally:
            retval_json = json.dumps(response)
            self.redis_conn.rpush(response_key, retval_json)


class BotWorkerPingError(Exception):
    pass


def ping(redis_conn, *, timeout):
    '''
    timeout arg is required because this is often called together
    with another function that has a timeout. need to be aware of double
    timeouts piling up.
    '''
    response_key = redis_enqueue_method_call(
        redis_conn=redis_conn, method_name='ping', method_kwargs={})

    # make it very long, so we don't get spurious ping errors
    result = redis_conn.blpop(response_key, timeout)

    if result is None:
        raise BotWorkerPingError(
            'Ping to botworker failed. '
            'If you want to use browser bots, '
            'you need to be running the botworker '
            '(which is started automatically if you run "otree runprodserver" '
            'Otherwise, set ("use_browser_bots": False) in the session config '
            'in settings.py.'
        )


def load_redis_response_dict(response_bytes: bytes):
    response = json.loads(response_bytes.decode('utf-8'))
    # response_error only exists if using Redis.
    # if using runserver, there is no need for this because the
    # exception is raised in the same thread.
    if 'traceback' in response:
        # cram the other traceback in this traceback message.
        # note:
        raise common_internal.BotError(response['traceback'])
    elif 'error' in response:
        # handled exception
        raise BotRequestError(response['error'])
    return response['retval']


def redis_flush_bots(redis_conn):
    for key in redis_conn.scan_iter(match='{}*'.format(REDIS_KEY_PREFIX)):
        redis_conn.delete(key)


def redis_enqueue_method_call(redis_conn, method_name, method_kwargs) -> str:
    response_key = '{}-{}'.format(REDIS_KEY_PREFIX, random.randint(1,10**9))
    msg = {
        'method': method_name,
        'kwargs': method_kwargs,
        'response_key': response_key,
    }
    redis_conn.rpush(REDIS_KEY_PREFIX, json.dumps(msg))
    return response_key


def redis_get_method_retval(redis_conn, response_key: str) -> dict:
    '''
    returns return value (if any) or raises an exception
    this is separate from redis_push for easier testing
    '''

    # timeout:
    # in practice is very fast...around 1ms
    # however, if an exception occurs, could take quite long.
    # so, make this very long so we don't get spurious errors.
    # no advantage to cutting it off early.
    # if it's that slow consistently, people will complain.
    result = redis_conn.blpop(response_key, timeout=6)
    if result is None:
        # ping will raise if it times out
        ping(redis_conn, timeout=3)
        raise Exception(
            'botworker is running but did not return a submission.'
        )
    key, submit_bytes = result
    return load_redis_response_dict(submit_bytes)


def wrap_method_call(method_name: str, method_kwargs):
    if otree.common_internal.USE_REDIS:
        redis_conn = get_redis_conn()
        response_key = redis_enqueue_method_call(
            redis_conn=redis_conn, method_name=method_name,
            method_kwargs=method_kwargs)
        return redis_get_method_retval(
            redis_conn=redis_conn, response_key=response_key)
    else:
        method = getattr(browser_bot_worker, method_name)
        return method(**method_kwargs)


def set_attributes(**kwargs):
    return wrap_method_call('set_attributes', kwargs)


def get_next_post_data(**kwargs) -> dict:
    return wrap_method_call('get_next_post_data', kwargs)


def initialize_session(**kwargs):
    # FIXME: need a timeout?
    # timeout must be int.
    # my tests show that it can initialize about 3000 players per second.
    # so 300-500 is conservative, plus pad for a few seconds
    #timeout = int(6 + num_players_total / 500)
    # maybe number of ParticipantToPlayerLookups?

    timeout = 6 # FIXME: adjust to number of players
    return wrap_method_call('initialize_session', kwargs)


def send_completion_message(*, session_code, participant_code):
    group_name = channel_utils.browser_bots_launcher_group(session_code)

    channel_utils.sync_group_send_wrapper(
        group=group_name,
        type='send_completion_message',
        event={'text': participant_code},
    )