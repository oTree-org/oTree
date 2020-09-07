import uuid

from django.core.management import call_command

from otree.models import Session

from .base import TestCase
from .simple_game import models as sg_models
from .single_player_game import models as sgc_models
import six
from six.moves import range


class TestCreateSessionsCommand(TestCase):

    def test_create_two_sessions_output(self):
        num_sessions = 2
        for i in range(num_sessions):
            call_command('create_session', 'simple_game', "1")
        created_sessions = Session.objects.count()
        self.assertEqual(created_sessions, num_sessions)

    def test_create_one_session(self):
        call_command('create_session', 'simple_game', "1")
        self.assertEqual(Session.objects.count(), 1)
        session = Session.objects.get()
        self.assertEqual(session.config['name'], 'simple_game')

        self.assertEqual(sg_models.Subsession.objects.count(), 1)
        subsession = sg_models.Subsession.objects.get()

        self.assertEqual(sg_models.Player.objects.count(), 1)

        player = sg_models.Player.objects.get()
        self.assertEqual(player.session, session)
        self.assertEqual(player.subsession, subsession)

    def test_session_vars(self):
        key = six.text_type(uuid.uuid4())
        value = six.text_type(uuid.uuid4())

        call_command('create_session', 'two_simple_games', "1")

        self.assertEqual(Session.objects.count(), 1)
        session = Session.objects.get()
        self.assertEqual(session.config['name'], 'two_simple_games')

        self.assertEqual(sg_models.Subsession.objects.count(), 1)
        self.assertEqual(sgc_models.Subsession.objects.count(), 1)
        subsession0 = sg_models.Subsession.objects.get()
        subsession1 = sgc_models.Subsession.objects.get()

        self.assertEqual(sg_models.Player.objects.count(), 1)
        self.assertEqual(sgc_models.Player.objects.count(), 1)

        # retrieve player of first subsession
        player0 = sg_models.Player.objects.get()

        # add a random key value
        player0.participant.vars[key] = value
        player0.participant.save()

        # retrieve player of second subsession
        player1 = sgc_models.Player.objects.get()

        # validate all
        self.assertTrue(player0.session == player1.session == session)
        self.assertEqual(player0.subsession, subsession0)
        self.assertEqual(player1.subsession, subsession1)

        # test the random key value in second subsession
        self.assertEqual(player1.participant.vars.get(key), value)


class TestCreateSessionView(TestCase):

    def test_create_session(self):
        pass
