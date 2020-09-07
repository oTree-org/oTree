#!/usr/bin/env python
# -*- coding: utf-8 -*-

import django.test
from huey.contrib.djhuey import db_task

from otree import constants_internal


test_client = django.test.Client()


@db_task()
def submit_expired_url(participant_code, url):
    from otree.models.participant import Participant

    # if the participant exists in the DB,
    # and they did not advance past the page yet

    # To reduce redundant server traffic, it's OK not to advance the page if the user already got to the next page
    # themselves, or via "advance slowest participants".
    # however, we must make sure that the user succeeded in loading the next page fully.
    # if the user made this page's POST but closed their browser before
    # the redirect to the next page's GET, then if the next page has a timeout,
    # it will not get scheduled, and then the auto-timeout chain would be broken.
    # so, instead of filtering by _index_in_pages (which is set in POST),
    # we filter by _current_form_page_url (which is set in GET,
    # AFTER the next page's timeout is scheduled.)

    if Participant.objects.filter(
            code=participant_code,
            _current_form_page_url=url).exists():
        test_client.post(
            url, data={constants_internal.timeout_happened: True}, follow=True)


@db_task()
def ensure_pages_visited(participant_pks):
    """This is necessary when a wait page is followed by a timeout page.
    We can't guarantee the user's browser will properly continue to poll
    the wait page and get redirected, so after a grace period we load the page
    automatically, to kick off the expiration timer of the timeout page.
    """

    from otree.models.participant import Participant

    # we used to filter by _index_in_pages, but that is not reliable,
    # because of the race condition described above.
    unvisited_participants = Participant.objects.filter(
        pk__in=participant_pks,
    )
    for participant in unvisited_participants:

        # if the wait page is the first page,
        # then _current_form_page_url could be null.
        # in this case, use the start_url() instead,
        # because that will redirect to the current wait page.
        # (alternatively we could define _current_page_url or
        # current_wait_page_url)
        url = participant._url_i_should_be_on()
        test_client.get(url, follow=True)
