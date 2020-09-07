#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import time
import logging
import six
import subprocess

import requests

from six.moves.urllib.parse import urljoin

from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.conf import settings

from ws4py.client.threadedclient import WebSocketClient

from otree.session import SESSION_CONFIGS_DICT


BROWSER_CMDS = {
    'windows': {
        'chrome': 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',  # noqa
        'firefox': "C:/Program Files (x86)/Mozilla Firefox/firefox.exe",
    },
    'mac': {
        'chrome': '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # noqa
        'firefox': None
    },
    'linux': {
        'firefox': 'firefox',
        'chrome': 'google-chrome',
    }
}

SERVER_URL_FLAG = '--server-url'


AUTH_FAILURE_MESSAGE = """
Could not login to the server using your ADMIN_USERNAME
and ADMIN_PASSWORD from settings.py. If you are testing
browser bots on a remote server, make sure the username
and password on your local oTree installation match that
on the server.
"""


def windows_mac_or_linux():
    if sys.platform.startswith("win"):
        platform = 'windows'
    elif sys.platform.startswith("darwin"):
        platform = 'mac'
    else:
        platform = 'linux'
    return platform


class OtreeWebSocketClient(WebSocketClient):

    def __init__(self, *args, **kwargs):
        self.session_size = kwargs.pop('session_size')
        self.seen_participant_codes = set()
        self.participants_finished = 0
        super(OtreeWebSocketClient, self).__init__(*args, **kwargs)

    def received_message(self, message):
        code = message
        if code not in self.seen_participant_codes:
            self.seen_participant_codes.add(code)
            self.participants_finished += 1
            if self.participants_finished == self.session_size:
                self.close(reason='success')


class Command(BaseCommand):
    help = "oTree: Run browser bots."

    def add_arguments(self, parser):
        parser.add_argument(
            'session_config_name', nargs='?',
            help='If omitted, all sessions in SESSION_CONFIGS are run'
        )
        parser.add_argument(
            SERVER_URL_FLAG, action='store', type=str, dest='server_url',
            default='http://127.0.0.1:8000',
            help="Server's root URL")
        ahelp = (
            'Number of participants. '
            'Defaults to minimum for the session config.'
        )
        parser.add_argument(
            'num_participants', type=int, nargs='?',
            help=ahelp)

    def handle(self, *args, **options):
        launcher = Launcher(options)
        launcher.run()


class Launcher(object):

    def __init__(self, options):
        self.options = options

    def run(self):
        options = self.options

        self.check_browser()
        self.set_urls()
        self.client = requests.session()
        self.ping_server()
        self.server_configuration_check()

        sessions_to_create = []

        if options["session_config_name"]:
            session_config_name = options["session_config_name"]
            if session_config_name not in SESSION_CONFIGS_DICT:
                raise ValueError(
                    'No session config named "{}"'.format(
                        session_config_name)
                )
            session_config_names = [session_config_name]

        else:
            # default to all session configs
            session_config_names = SESSION_CONFIGS_DICT.keys()

        self.max_name_length = max(
            len(config_name) for config_name in session_config_names
        )

        for session_config_name in session_config_names:
            session_config = SESSION_CONFIGS_DICT[session_config_name]
            num_bot_cases = session_config.get_num_bot_cases()
            for bot_case_number in range(num_bot_cases):
                num_participants = (options.get('num_participants') or
                                    session_config['num_demo_participants'])
                sessions_to_create.append({
                    'session_config_name': session_config_name,
                    'num_participants': num_participants,
                    'bot_case_number': bot_case_number,
                })

        total_time_spent = 0
        # run in a separate loop, because we want to validate upfront
        # that the session configs are valid, etc,
        # rather than the command failing halfway through
        for session_to_create in sessions_to_create:
            total_time_spent += self.run_session(**session_to_create)

        print('Total: {} seconds'.format(
            round(total_time_spent, 1)
        ))

        # don't delete sessions -- it's too susceptible to race conditions
        # between sending the completion message and loading the last page
        # plus people want to preserve the data
        # just label these sessions clearly in the admin UI
        # and make it easy to delete manually

    def run_session(
            self, session_config_name, num_participants, bot_case_number):
        self.close_existing_session()

        browser_process = self.launch_browser(num_participants)

        row_fmt = "{:<%d} {:>2} participants..." % (self.max_name_length + 1)
        print(row_fmt.format(session_config_name, num_participants), end='')

        session_code = self.create_session(
            session_config_name, num_participants, bot_case_number)

        bot_start_time = time.time()

        self.websocket_listen(session_code, num_participants)

        time_spent = round(time.time() - bot_start_time, 1)
        print('...finished in {} seconds'.format(time_spent))

        # TODO:
        # - if Chrome/FF is already running when the browser is launched,
        # this does nothing.
        # also, they report a crash (in Firefox it blocks the app from
        # starting again), in Chrome it's just a side notice
        browser_process.terminate()
        return time_spent

    def websocket_listen(self, session_code, num_participants):
        # seems that urljoin doesn't work with ws:// urls
        # so do the ws replace after URLjoin
        websocket_url = urljoin(
            self.server_url,
            '/browser_bots_client/{}/'.format(session_code)
        )
        websocket_url = websocket_url.replace(
            'http://', 'ws://').replace('https://', 'wss://')

        ws_client = OtreeWebSocketClient(
            websocket_url,
            session_size=num_participants,
        )
        ws_client.connect()
        ws_client.run_forever()

    def set_urls(self):
        # SERVER URL
        server_url = self.options['server_url']
        # if it doesn't start with http:// or https://,
        # assume http://
        if not server_url.startswith('http'):
            server_url = 'http://' + server_url
        self.server_url = server_url

        # CREATE_SESSION URL
        self.create_session_url = urljoin(
            server_url,
            reverse('CreateBrowserBotsSession')
        )

        # LOGIN URL
        # TODO: use reverse? reverse('django.contrib.auth.views.login')
        self.login_url = urljoin(server_url, '/accounts/login/')

    def post(self, url, data=None):
        data = data or {}
        data.update({'csrfmiddlewaretoken': self.client.cookies['csrftoken']})
        return self.client.post(url, data)

    def server_configuration_check(self):
        # .get just returns server readiness info
        # try to get this page without logging in
        # we don't want to login if it isn't necessary, because maybe
        # settings.ADMIN_PASSWORD is empty, and therefore no user account
        # exists.
        resp = self.client.get(self.create_session_url)

        # if AUTH_LEVEL is set on remote server, then this will redirect
        # to a login page
        login_url = self.login_url
        if login_url in resp.url:
            # login
            resp = self.post(
                login_url,
                data={
                    'username': settings.ADMIN_USERNAME,
                    'password': settings.ADMIN_PASSWORD,
                },
            )

            if login_url in resp.url:
                raise Exception(AUTH_FAILURE_MESSAGE)

            # get it again, we are logged in now
            resp = self.client.get(self.create_session_url)
        server_check = resp.json()  # noqa

        # no need to warn about these for now
        # if server_check['runserver']:
        #     print(RUNSERVER_WARNING)
        # if server_check['sqlite']:
        #     print(SQLITE_WARNING)

    def ping_server(self):

        logging.getLogger("requests").setLevel(logging.WARNING)

        try:
            # open this just to populate CSRF cookie
            # (because login page contains a form)
            resp = self.client.get(self.login_url)

        except:
            raise Exception(
                'Could not connect to server at {}.'
                'Before running this command, '
                'you need to run the server (see {} flag).'.format(
                    self.server_url,
                    SERVER_URL_FLAG
                )
            )
        if not resp.ok:
            raise Exception(
                'Could not open page at {}.'
                '(HTTP status code: {})'.format(
                    self.login_url,
                    resp.status_code,
                )
            )

    def create_session(
            self, session_config_name, num_participants, bot_case_number
            ):

        resp = self.post(
            self.create_session_url,
            data={
                'session_config_name': session_config_name,
                'num_participants': num_participants,
                'bot_case_number': bot_case_number
            }
        )
        assert resp.ok, 'Failed to create session. Check the server logs.'
        session_code = resp.content.decode('utf-8')
        return session_code

    def check_browser(self):
        platform = windows_mac_or_linux()
        # right now hardcoded to Chrome unless settings.BROWSER_COMMAND set
        chrome_cmd = BROWSER_CMDS[platform]['chrome']

        self.browser_cmd = getattr(settings, 'BROWSER_COMMAND', chrome_cmd)

        # check if browser is running
        if 'chrome' in self.browser_cmd.lower():
            browser_type = 'Chrome'
        elif 'firefox' in self.browser_cmd.lower():
            browser_type = 'Firefox'
        else:
            return

        if windows_mac_or_linux() == 'windows':
            process_list_args = ['tasklist']
        else:
            process_list_args = ['ps', 'axw']
        ps_output = subprocess.check_output(process_list_args).decode('utf-8')
        is_running = browser_type.lower() in ps_output.lower()

        if is_running:
            print(
                'WARNING: it looks like {browser} is already running. '
                'You should quit {browser} before running '
                'this command.'.format(browser=browser_type)
            )

    def close_existing_session(self):
        # make sure room is closed
        resp = self.post(
            urljoin(self.server_url, reverse('CloseBrowserBotsSession')))
        assert resp.ok

    def launch_browser(self, num_participants):
        wait_room_url = urljoin(
            self.server_url,
            reverse('BrowserBotStartLink')
        )

        args = [self.browser_cmd]
        for i in range(num_participants):
            args.append(wait_room_url)

        try:
            return subprocess.Popen(args)
        except Exception as exception:
            msg = (
                'Could not launch browser. '
                'Check your settings.BROWSER_COMMAND. {}'
            )
            ExceptionClass = type(exception)
            six.reraise(
                ExceptionClass,
                ExceptionClass(msg.format(exception)),
                sys.exc_info()[2])
