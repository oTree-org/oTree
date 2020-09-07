from django.core.management import call_command
from django.test.client import RequestFactory

from otree import constants_internal
from otree.models import Participant

from .simple_game.views import MyPage
from .simple_game.models import Player
from .utils import capture_stdout
from .base import TestCase


class Attribute(object):
    pass


class OTreeRequestFactory(RequestFactory):
    def __init__(self, *args, **kwargs):
        self.view_name = kwargs.pop('view_name')
        super(OTreeRequestFactory, self).__init__(*args, **kwargs)

    def request(self, **request):
        http_request = super(OTreeRequestFactory, self).request(**request)
        http_request.resolver_match = Attribute()
        http_request.resolver_match.url_name = self.view_name
        return http_request


class BaseViewTestCase(TestCase):
    view_name = 'tests.simple_game.views.Abstract'

    def setUp(self):
        self.factory = OTreeRequestFactory(view_name=self.view_name)
        self.request = self.factory.get('/my-page/')

        with capture_stdout():
            call_command('create_session', 'simple_game', "1")

        self.participant = Participant.objects.first()
        self.player = Player.objects.first()

    def reload_objects(self):
        self.participant = Participant.objects.get(pk=self.participant.pk)
        self.player = Player.objects.get(pk=self.player.pk)


class TestPageView(BaseViewTestCase):
    def setUp(self):
        super(TestPageView, self).setUp()

        self.kwargs = {
            constants_internal.participant_code: self.participant.code,
            constants_internal.user_type: 'p',
            constants_internal.index_in_pages: 0,
        }
        self.view = MyPage.as_view()

        self.reload_objects()
