#!/usr/bin/env python
# encoding: utf-8

import warnings
import datetime
from collections import defaultdict
import sys
import logging

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import get_object_or_404

from six.moves.urllib.parse import urlparse
from six.moves.urllib.parse import urlunparse

import vanilla

import boto.mturk.connection
from boto.mturk.connection import MTurkRequestError
from boto.mturk.qualification import Qualifications

import IPy

import otree
from otree import forms
from otree.deprecate import OtreeDeprecationWarning
from otree.views.abstract import AdminSessionPageMixin
from otree.checks.mturk import validate_session_for_mturk
from otree.forms import widgets
from otree.common import RealWorldCurrency
from otree.models import Session


logger = logging.getLogger('otree')


class MTurkError(Exception):

    def __init__(self, request, message):
        self.message = message
        messages.error(request, message, extra_tags='safe')

    def __str__(self):
        return self.message


class MTurkConnection(boto.mturk.connection.MTurkConnection):

    def __init__(self, request, in_sandbox=True):
        if in_sandbox:
            self.mturk_host = settings.MTURK_SANDBOX_HOST
        else:
            self.mturk_host = settings.MTURK_HOST
        self.request = request

    def __enter__(self):
        self = boto.mturk.connection.MTurkConnection(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            host=self.mturk_host,
        )
        return self

    def __exit__(self, exc_type, value, traceback):
        # TODO: need to take care of possible errors (login,
        # "service not approved")
        if exc_type is MTurkRequestError:
            MTurkError(self.request, value.message)
        return False


def get_workers_by_status(conn, hit_id):
    all_assignments = get_all_assignments(conn, hit_id)
    workers_by_status = defaultdict(list)
    for assignment in all_assignments:
        workers_by_status[
            assignment.AssignmentStatus
        ].append(assignment.WorkerId)
    return workers_by_status


def get_all_assignments(conn, hit_id, status=None):
    # Accumulate all relevant assignments, one page of results at
    # a time.
    assignments = []
    page = 1
    while True:
        rs = conn.get_assignments(
            hit_id=hit_id,
            page_size=100,
            page_number=page,
            status=status)
        assignments.extend(rs)
        if len(assignments) >= int(rs.TotalNumResults):
            break
        page += 1
    return assignments


class MTurkCreateHITForm(forms.Form):

    in_sandbox = forms.BooleanField(
        required=False,
        help_text="Do you want HIT published on MTurk sandbox?")
    title = forms.CharField()
    description = forms.CharField()
    keywords = forms.CharField()
    money_reward = forms.RealWorldCurrencyField(
        # it seems that if this is omitted, the step defaults to an integer,
        # meaninng fractional inputs are not accepted
        widget=widgets.RealWorldCurrencyInput(attrs={'step': 0.01})
    )
    assignments = forms.IntegerField(
        label="Number of assignments",
        help_text="How many unique Workers do you want to work on the HIT?")
    minutes_allotted_per_assignment = forms.IntegerField(
        label="Minutes allotted per assignment",
        help_text=(
            "Number of minutes, that a Worker has to "
            "complete the HIT after accepting it."
        ))
    expiration_hours = forms.FloatField(
        label="Hours until HIT expiration",
        help_text=(
            "Number of hours after which the HIT "
            "is no longer available for users to accept. "
        ))

    def __init__(self, *args, **kwargs):
        super(MTurkCreateHITForm, self).__init__(*args, **kwargs)
        self.fields['assignments'].widget.attrs['readonly'] = True


class MTurkCreateHIT(AdminSessionPageMixin, vanilla.FormView):
    '''This view creates mturk HIT for session provided in request
    AWS externalQuestion API is used to generate HIT.

    '''
    form_class = MTurkCreateHITForm

    def in_public_domain(self, request, *args, **kwargs):
        """This method validates if oTree are published on a public domain
        because mturk need it

        """
        host = request.get_host().lower()
        if ":" in host:
            host = host.split(":", 1)[0]
        if host == "localhost":
            return False
        try:
            ip = IPy.IP(host)
            return ip.iptype() == "PUBLIC"
        except ValueError:
            # probably is a public domain
            return True

    def get(self, request, *args, **kwargs):
        validate_session_for_mturk(request, self.session)
        mturk_settings = self.session.config['mturk_hit_settings']
        initial = {
            'title': mturk_settings['title'],
            'description': mturk_settings['description'],
            'keywords': ', '.join(mturk_settings['keywords']),
            'money_reward': self.session.config['participation_fee'],
            'in_sandbox': settings.DEBUG,
            'minutes_allotted_per_assignment': (
                mturk_settings['minutes_allotted_per_assignment']
            ),
            'expiration_hours': mturk_settings['expiration_hours'],
            'assignments': self.session.mturk_num_participants,
        }
        form = self.get_form(initial=initial)
        context = self.get_context_data(form=form)
        context['mturk_enabled'] = (
            bool(settings.AWS_ACCESS_KEY_ID) and
            bool(settings.AWS_SECRET_ACCESS_KEY)
        )
        context['runserver'] = 'runserver' in sys.argv
        url = self.request.build_absolute_uri(
            reverse('MTurkCreateHIT', args=(self.session.code,))
        )
        secured_url = urlunparse(urlparse(url)._replace(scheme='https'))
        context['secured_url'] = secured_url

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.get_form(
            data=request.POST,
            files=request.FILES
        )
        if not form.is_valid():
            return self.form_invalid(form)
        session = self.session
        in_sandbox = 'in_sandbox' in form.data
        # session can't be created
        if (not self.in_public_domain(request, *args, **kwargs) and
           not in_sandbox):
                msg = (
                    '<h1>Error: '
                    'oTree must run on a public domain for Mechanical Turk'
                    '</h1>')
                return HttpResponseServerError(msg)
        with MTurkConnection(self.request, in_sandbox) as mturk_connection:
            mturk_settings = session.config['mturk_hit_settings']
            qualification_id = mturk_settings.get(
                'grant_qualification_id', None)
            # verify that specified qualification type
            # for preventing retakes exists on mturk server
            if qualification_id:
                try:
                    mturk_connection.get_qualification_type(qualification_id)
                except MTurkRequestError as e:
                    code = 'AWS.MechanicalTurk.QualificationTypeDoesNotExist'
                    if e.error_code == code:
                        if in_sandbox:
                            sandbox_note = (
                                'You are currently using the sandbox, so you '
                                'can only grant qualifications that were '
                                'also created in the sandbox.')
                        else:
                            sandbox_note = (
                                'You are using the MTurk live site, so you '
                                'can only grant qualifications that were '
                                'also created on the live site, and not the '
                                'MTurk sandbox.')
                        msg = (
                            "In settings.py you specified qualification ID "
                            " '{}' which doesn't exist in your MTurk account. "
                            "Please check its validity. Note: {}".format(
                                qualification_id, sandbox_note))
                        if in_sandbox:
                            msg += ' You are currently'
                        messages.error(request, msg)
                        return HttpResponseRedirect(
                            reverse(
                                'MTurkCreateHIT', args=(session.code,)))
                else:
                    session.mturk_qualification_type_id = qualification_id

            url_landing_page = self.request.build_absolute_uri(
                reverse('MTurkLandingPage', args=(session.code,)))

            # updating schema from http to https
            # this is compulsory for MTurk exteranlQuestion
            # TODO: validate, that the server support https
            #       (heroku does support by default)
            secured_url_landing_page = urlunparse(
                urlparse(url_landing_page)._replace(scheme='https'))

            # TODO: validate that there is enought money for the hit
            money_reward = form.data['money_reward']
            reward = boto.mturk.price.Price(
                amount=float(money_reward))

            # assign back to participation_fee, in case it was changed
            # in the form
            # TODO: why do I have to explicitly
            # convert back to RealWorldCurrency?
            # shouldn't it already be that?
            session.config['participation_fee'] = RealWorldCurrency(
                money_reward)

            # creating external questions, that would be passed to the hit
            external_question = boto.mturk.question.ExternalQuestion(
                secured_url_landing_page, mturk_settings['frame_height'])

            qualifications = mturk_settings.get('qualification_requirements')

            # deprecated summer 2015: remove this
            if not qualifications and \
               hasattr(settings, 'MTURK_WORKER_REQUIREMENTS'):
                    warn_msg = (
                        'The MTURK_WORKER_REQUIREMENTS setting has been '
                        'deprecated. You should instead use '
                        '"qualification_requirements" as shown here: '
                        'https://github.com/oTree-org/oTree/blob/master/'
                        'settings.py')
                    warnings.warn(warn_msg, OtreeDeprecationWarning)
                    qualifications = settings.MTURK_WORKER_REQUIREMENTS

            mturk_hit_parameters = {
                'title': form.cleaned_data['title'],
                'description': form.cleaned_data['description'],
                'keywords': [
                    k.strip() for k in
                    form.cleaned_data['keywords'].split(',')
                ],
                'question': external_question,
                'max_assignments': form.cleaned_data['assignments'],
                'reward': reward,
                'response_groups': ('Minimal', 'HITDetail'),
                'qualifications': Qualifications(qualifications),
                'duration': datetime.timedelta(
                    minutes=(
                        form.cleaned_data['minutes_allotted_per_assignment']
                    )),
                'lifetime': datetime.timedelta(
                    minutes=int(60*form.cleaned_data['expiration_hours']))
            }

            hit = mturk_connection.create_hit(**mturk_hit_parameters)
            session.mturk_HITId = hit[0].HITId
            session.mturk_HITGroupId = hit[0].HITGroupId
            session.mturk_sandbox = in_sandbox
            session.save()

        return HttpResponseRedirect(
            reverse('MTurkCreateHIT', args=(session.code,)))


class PayMTurk(vanilla.View):

    url_pattern = r'^PayMTurk/(?P<session_code>[a-z0-9]+)/$'

    def post(self, request, *args, **kwargs):
        session = get_object_or_404(otree.models.Session,
                                    code=kwargs['session_code'])
        successful_payments = 0
        failed_payments = 0
        with MTurkConnection(self.request,
                             session.mturk_sandbox) as mturk_connection:
            for p in session.participant_set.filter(
                mturk_assignment_id__in=request.POST.getlist('payment')
            ):
                try:
                    # approve assignment
                    mturk_connection.approve_assignment(p.mturk_assignment_id)
                except boto.mturk.connection.MTurkRequestError as e:
                    msg = (
                        'Could not pay {} because of an error communicating '
                        'with MTurk: {}'.format(p._id_in_session(), str(e)))
                    messages.error(request, msg)
                    logger.error(msg)
                    failed_payments += 1
                else:
                    successful_payments += 1
                    # grant bonus
                    # TODO: check if bonus was already paid before,
                    # perhaps through
                    # mturk requester webinterface
                    payoff = p.payoff_in_real_world_currency().to_number()
                    if payoff > 0:
                        bonus = boto.mturk.price.Price(amount=payoff)
                        mturk_connection.grant_bonus(
                            p.mturk_worker_id,
                            p.mturk_assignment_id,
                            bonus,
                            reason="Thank you for "
                            "participating.")
        msg = 'Successfully made {} payments.'.format(successful_payments)
        if failed_payments > 0:
            msg += ' {} payments failed.'.format(failed_payments)
            messages.warning(request, msg)
        else:
            messages.success(request, msg)
        return HttpResponseRedirect(
            reverse('MTurkSessionPayments', args=(session.code,)))


class RejectMTurk(vanilla.View):

    url_pattern = r'^RejectMTurk/(?P<session_code>[a-z0-9]+)/$'

    def post(self, request, *args, **kwargs):
        session = get_object_or_404(Session,
                                    code=kwargs['session_code'])
        with MTurkConnection(self.request,
                             session.mturk_sandbox) as mturk_connection:
            for p in session.participant_set.filter(
                mturk_assignment_id__in=request.POST.getlist('payment')
            ):
                mturk_connection.reject_assignment(p.mturk_assignment_id)

        messages.success(request, "You successfully rejected "
                                  "selected assignments")
        return HttpResponseRedirect(
            reverse('MTurkSessionPayments', args=(session.code,)))
