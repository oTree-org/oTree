
from django.urls import reverse

import otree.common_internal
from otree import constants_internal
from otree.common_internal import random_chars_8
from otree.db import models
from otree.models_concrete import ParticipantToPlayerLookup
from .varsmixin import ModelWithVars
import model_utils

class Participant(ModelWithVars):
    _ft = model_utils.FieldTracker()

    class Meta:
        ordering = ['pk']
        app_label = "otree"
        index_together = ['session', 'mturk_worker_id', 'mturk_assignment_id']

    session = models.ForeignKey(
        'otree.Session', on_delete=models.CASCADE
    )

    label = models.CharField(
        max_length=50, null=True, doc=(
            "Label assigned by the experimenter. Can be assigned by passing a "
            "GET param called 'participant_label' to the participant's start "
            "URL"
        )
    )

    id_in_session = models.PositiveIntegerField(null=True)

    payoff = models.CurrencyField(default=0)

    time_started = models.DateTimeField(null=True)
    user_type_in_url = constants_internal.user_type_participant
    mturk_assignment_id = models.CharField(
        max_length=50, null=True)
    mturk_worker_id = models.CharField(max_length=50, null=True)

    _index_in_subsessions = models.PositiveIntegerField(default=0, null=True)

    _index_in_pages = models.PositiveIntegerField(default=0, db_index=True)

    def _id_in_session(self):
        """the human-readable version."""
        return 'P{}'.format(self.id_in_session)

    _waiting_for_ids = models.CharField(null=True, max_length=300)

    code = models.CharField(
        default=random_chars_8,
        max_length=16,
        # set non-nullable, until we make our CharField non-nullable
        null=False,
        # unique implies DB index
        unique=True,
        doc=(
            "Randomly generated unique identifier for the participant. If you "
            "would like to merge this dataset with those from another "
            "subsession in the same session, you should join on this field, "
            "which will be the same across subsessions."
        )
    )


    visited = models.BooleanField(
        default=False, db_index=True,
        doc="""Whether this user's start URL was opened"""
    )

    ip_address = models.GenericIPAddressField(null=True)

    # stores when the page was first visited
    _last_page_timestamp = models.PositiveIntegerField(null=True)

    _last_request_timestamp = models.PositiveIntegerField(null=True)

    is_on_wait_page = models.BooleanField(default=False)

    # these are both for the admin
    # In the changelist, simply call these "page" and "app"
    _current_page_name = models.CharField(max_length=200, null=True,
                                          verbose_name='page')
    _current_app_name = models.CharField(max_length=200, null=True,
                                         verbose_name='app')

    # only to be displayed in the admin participants changelist
    _round_number = models.PositiveIntegerField(
        null=True
    )

    _current_form_page_url = models.URLField()

    _max_page_index = models.PositiveIntegerField()

    _browser_bot_finished = models.BooleanField(default=False)

    _is_bot = models.BooleanField(default=False)
    # can't start with an underscore because used in template
    # can't end with underscore because it's a django field (fields.E001)
    is_browser_bot = models.BooleanField(default=False)

    _player_lookups = None

    def player_lookup(self):
        '''
        Code is more complicated because of a performance optimization
        '''
        index = self._index_in_pages
        if self._player_lookups is None:
            self._player_lookups = {}
        if index not in self._player_lookups:
            # kind of a binary search type logic. limit the number of queries
            # to log2(n). similar to the way arraylists grow.
            num_extra_lookups = len(self._player_lookups) + 1
            qs = ParticipantToPlayerLookup.objects.filter(
                participant=self,
                page_index__range=(index, index+num_extra_lookups)
            ).values()
            for player_lookup in qs:
                self._player_lookups[player_lookup['page_index']] = player_lookup
        return self._player_lookups[index]

    def _current_page(self):
        return '{}/{} pages'.format(self._index_in_pages, self._max_page_index)

    # because variables used in templates can't start with an underscore
    def current_page_(self):
        return self._current_page()

    def get_players(self):
        """Used to calculate payoffs"""
        lst = []
        app_sequence = self.session.config['app_sequence']
        for app in app_sequence:
            models_module = otree.common_internal.get_models_module(app)
            players = models_module.Player.objects.filter(
                participant=self
            ).order_by('round_number')
            lst.extend(list(players))
        return lst

    def status(self):
        # TODO: status could be a field that gets set imperatively
        if not self.visited:
            return 'Not started'
        if self.is_on_wait_page:
            if self._waiting_for_ids:
                return 'Waiting for {}'.format(self._waiting_for_ids)
            return 'Waiting'
        return 'Playing'

    def _url_i_should_be_on(self):
        if not self.visited:
            return self._start_url()
        if self._index_in_pages <= self._max_page_index:
            return self.player_lookup()['url']
        if self.session.mturk_HITId:
            assignment_id = self.mturk_assignment_id
            if self.session.mturk_use_sandbox:
                url = 'https://workersandbox.mturk.com/mturk/externalSubmit'
            else:
                url = "https://www.mturk.com/mturk/externalSubmit"
            url = otree.common_internal.add_params_to_url(
                url,
                {
                    'assignmentId': assignment_id,
                    'extra_param': '1'  # required extra param?
                }
            )
            return url
        return reverse('OutOfRangeNotification')

    def _start_url(self):
        return otree.common_internal.participant_start_url(self.code)

    def payoff_in_real_world_currency(self):
        return self.payoff.to_real_world_currency(
            self.session
        )

    def money_to_pay(self):
        '''deprecated'''
        return self.payoff_plus_participation_fee()

    def payoff_plus_participation_fee(self):
        return self.session._get_payoff_plus_participation_fee(self.payoff)
