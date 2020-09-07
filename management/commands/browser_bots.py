from django.core.management.base import BaseCommand
from otree.bots.browser_launcher import Launcher


class Command(BaseCommand):
    help = "oTree: Run browser bots."

    def add_arguments(self, parser):
        parser.add_argument(
            'session_config_name', nargs='?',
            help='If omitted, all sessions in SESSION_CONFIGS are run'
        )
        parser.add_argument(
            '--server-url', action='store', type=str, dest='server_url',
            default='http://127.0.0.1:8000',
            help="Server's root URL")
        ahelp = (
            'Number of participants. '
            'Defaults to minimum for the session config.'
        )
        parser.add_argument(
            'num_participants', type=int, nargs='?',
            help=ahelp)

    def handle(self, session_config_name, server_url, num_participants, **options):

        launcher = Launcher(
            session_config_name=session_config_name,
            server_url=server_url,
            num_participants=num_participants
        )
        launcher.run()


