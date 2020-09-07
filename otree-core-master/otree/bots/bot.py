#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import decimal
import logging
import abc
from importlib import import_module

import six
from six.moves import urllib
from six.moves.html_parser import HTMLParser

from django import test
from django.core.urlresolvers import resolve
from django.conf import settings
from easymoney import Money as Currency

from otree import constants_internal

from otree.common_internal import get_dotted_name, get_bots_module


logger = logging.getLogger('otree.bots')


HTML_MISSING_FIELD_WARNING = '''
Bot is trying to submit fields: "{}",
but these form fields were not found in the HTML of the page
(searched for tags "{}" with "name" attribute matching the field name).
Checking the HTML may not find all form fields
(e.g. those added with JavaScript),
so you can disable this check by yielding a Submission
with check_html=False, e.g.:

yield Submission(views.PageName, {{...}}, check_html=False)
'''.replace('\n', ' ').strip()


def SubmitInternal(submission_tuple, check_html):

    post_data = {}

    if isinstance(submission_tuple, (list, tuple)):
        PageClass = submission_tuple[0]
        if len(submission_tuple) == 2:
            post_data = submission_tuple[1]
    else:
        PageClass = submission_tuple

    post_data = post_data or {}

    # TODO: validate that user isn't trying to submit a WaitPage,
    # or other possible mistakes

    for key in post_data:
        if isinstance(post_data[key], Currency):
            # because must be json serializable for Huey
            post_data[key] = str(decimal.Decimal(post_data[key]))

    return {
        'page_class': PageClass,
        'page_class_dotted': get_dotted_name(PageClass),
        'post_data': post_data,
        'check_html': check_html
    }


def Submission(
        PageClass, post_data=None, check_html=settings.BOTS_CHECK_HTML):
    return SubmitInternal((PageClass, post_data), check_html)


def SubmissionMustFail(
        PageClass, post_data=None, check_html=settings.BOTS_CHECK_HTML):
    '''lets you intentionally submit with invalid
    input to ensure it's correctly rejected'''

    post_data = post_data or {}

    # must_fail needs to go in post_data rather than being a separate
    # dict key, because CLI bots and browser bots need to work the same way.
    # CLI bots can only talk to server through post data
    post_data.update({'must_fail': True})

    return Submission(PageClass, post_data, check_html)


class MissingFieldChecker(HTMLParser):

    def __init__(self, fields_to_check):
        super(MissingFieldChecker, self).__init__()
        self.missing_fields = set(fields_to_check)
        self.tags = {'input', 'button', 'select', 'textarea'}

    def get_missing_fields(self, html):
        self.feed(html)
        return self.missing_fields

    def handle_starttag(self, tag, attrs):
        if tag in self.tags:
            for (attr_name, attr_value) in attrs:
                if attr_name == 'name':
                    self.missing_fields.discard(attr_value)


def is_wait_page(response):
    return (
        response.get(constants_internal.wait_page_http_header) ==
        constants_internal.get_param_truth_value)


def refresh_from_db(obj):
    return type(obj).objects.get(pk=obj.pk)


class ParticipantBot(six.with_metaclass(abc.ABCMeta, test.Client)):

    def __init__(
            self, participant, **kwargs):
        self.participant = participant
        self.url = None
        self._response = None
        self._html = None
        self.path = None
        self.submits = None
        super(ParticipantBot, self).__init__()

        self.player_bots = []
        for player in self.participant.get_players():
            bots_module = get_bots_module(player._meta.app_config.name)
            player_bot = bots_module.PlayerBot(
                player=player,
                participant_bot=self)
            self.player_bots.append(player_bot)
        self.submits_generator = self.get_submits()

    def open_start_url(self):
        self.response = self.get(
            self.participant._start_url(),
            follow=True
        )

    def get_submits(self):
        for player_bot in self.player_bots:
            # play_round populates legacy submit list
            generator = player_bot.play_round()
            if player_bot._legacy_submit_list:
                for submission in player_bot._legacy_submit_list:
                    yield submission
            else:
                try:
                    for submission in generator:
                        if not isinstance(submission, dict):
                            submission = SubmitInternal(
                                submission, check_html=False)
                        self.assert_correct_page(submission)
                        self.assert_correct_fields(submission)
                        yield submission
                # handle the case where it's empty
                except TypeError as exc:
                    if 'is not iterable' in str(exc):
                        raise StopIteration
                    raise

    def assert_correct_fields(self, submission):
        if submission['check_html']:
            field_names = [
                f for f in submission['post_data'].keys() if f != 'must_fail']
            checker = MissingFieldChecker(field_names)
            missing_fields = checker.get_missing_fields(self.html)
            if missing_fields:
                raise AssertionError(
                    HTML_MISSING_FIELD_WARNING.format(
                        ', '.join(missing_fields),
                        ', '.join(checker.tags)))

    def assert_correct_page(self, submission):
        PageClass = submission['page_class']
        expected_url = PageClass.url_name()
        actual_url = resolve(self.path).url_name

        if not expected_url == actual_url:
            raise AssertionError(
                "Bot expects to be on page {}, "
                "but current page is {}. "
                "Check your bot in tests.py, "
                "then create a new session.".format(expected_url, actual_url))

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, response):
        try:
            self.url = response.redirect_chain[-1][0]
            self.path = urllib.parse.urlsplit(self.url).path
        except IndexError:
            # 2016-08-07...what are the consequences if self.path is not set?
            pass
        self._response = response
        self.html = response.content.decode('utf-8')

    @property
    def html(self):
        return self._html

    @html.setter
    def html(self, html):
        html = html.replace('\n', ' ').replace('\r', ' ')
        html = re.sub(r'\s+', ' ', html)
        self._html = html

    def on_wait_page(self):
        # if the existing response was a form page, it will still be...
        # no need to check again
        if not is_wait_page(self.response):
            return False

        # however, wait pages can turn into regular pages, so let's try again
        self.response = self.get(self.url, follow=True)
        return is_wait_page(self.response)

    def submit(self, submission):
        post_data = submission['post_data']
        if post_data:
            logger.info('{}, {}'.format(self.path, post_data))
        else:
            logger.info(self.path)

        self.response = self.post(self.url, post_data, follow=True)


class PlayerBot(object):

    cases = []

    def __init__(self, player, participant_bot, **kwargs):

        self.participant_bot = participant_bot
        self._cached_player = player
        self._cached_group = player.group
        self._cached_subsession = player.subsession
        self._cached_participant = player.participant
        self._cached_session = player.session
        self._legacy_submit_list = []

        case_number = self._cached_session._bot_case_number
        cases = self.cases
        if len(cases) >= 1:
            self.case = cases[case_number % len(cases)]
        else:
            self.case = None

    def play_round(self):
        pass

    @property
    def player(self):
        return refresh_from_db(self._cached_player)

    @property
    def group(self):
        return refresh_from_db(self._cached_group)

    @property
    def subsession(self):
        return refresh_from_db(self._cached_subsession)

    @property
    def session(self):
        return refresh_from_db(self._cached_session)

    @property
    def participant(self):
        return refresh_from_db(self._cached_participant)

    def submit(self, ViewClass, param_dict=None):
        self._legacy_submit_list.append(
            SubmitInternal((ViewClass, param_dict), check_html=False))

    def submit_invalid(self, ViewClass, param_dict=None):
        # simpler to make this a no-op, it makes porting to yield easier
        # then we can just do a search-and-replace
        # self._legacy_submit_list.append((ViewClass, param_dict, 'invalid'))
        pass

    @property
    def html(self):
        return self.participant_bot.html
