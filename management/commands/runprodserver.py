import logging
from django.core.management import call_command
from . import webandworkers

logger = logging.getLogger(__name__)


class Command(webandworkers.Command):

    '''
    It's almost the same as webandworkers,
    but it also runs collectstatic,
    and launches the timeoutworker.
    this command is intended for generic server deployment,
    whereas webandworkers is intended for Heroku.
    '''

    def add_arguments(self, parser):
        super().add_arguments(parser)
        ahelp = (
            'By default we will collect all static files into the directory '
            'configured in your settings. Disable it with this switch if you '
            'want to do it manually.')
        parser.add_argument(
            '--no-collectstatic', action='store_false', dest='collectstatic',
            default=True, help=ahelp)

    def setup_honcho(self, **options):
        super().setup_honcho(**options)
        honcho = self.honcho

        honcho.add_otree_process(
            'botworker',
            'otree botworker',
        )
        honcho.add_otree_process(
            'timeoutworkeronly',
            'otree timeoutworkeronly',
        )

    def handle(self, *args, collectstatic, **options):

        if collectstatic:
            self.stdout.write('Running collectstatic ...')
            call_command('collectstatic', interactive=False, verbosity=1)

        return super().handle(*args, **options)
