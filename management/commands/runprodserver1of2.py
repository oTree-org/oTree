import os
import re
import sys
import logging

import honcho.manager
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
import otree

logger = logging.getLogger(__name__)

naiveip_re = re.compile(r"""^(?:
(?P<addr>
    (?P<ipv4>\d{1,3}(?:\.\d{1,3}){3}) |         # IPv4 address
    (?P<ipv6>\[[a-fA-F0-9:]+\]) |               # IPv6 address
    (?P<fqdn>[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*) # FQDN
):)?(?P<port>\d+)$""", re.X)

DEFAULT_PORT = "8000"
DEFAULT_ADDR = '0.0.0.0'

# hypercorn/uvicorn don't support multiple workers on windows.
# daphne doesn't support multiple workers at all.
# https://github.com/django/channels/issues/960
# https://gitlab.com/pgjones/hypercorn/issues/84
# https://github.com/encode/uvicorn/issues/342#issuecomment-480230739
if sys.platform.startswith("win"):
    NUM_WORKERS = 1
else:
    NUM_WORKERS = 3

def get_ssl_file_path(filename):
    otree_dir = os.path.dirname(otree.__file__)
    pth = os.path.join(otree_dir, 'certs', filename)
    return pth.replace('\\', '/')

# made this simple class to reduce code duplication,
# and to make testing easier (I didn't know how to check that it was called
# with os.environ.copy(), especially if we patch os.environ)
class OTreeHonchoManager(honcho.manager.Manager):
    def add_otree_process(self, name, cmd):
        self.add_process(name, cmd, env=os.environ.copy(), quiet=False)


class Command(BaseCommand):
    help = 'oTree production server.'

    def add_arguments(self, parser):

        parser.add_argument('addrport', nargs='?',
            help='Optional port number, or ipaddr:port')

        ahelp = (
            'Run an SSL server directly in Daphne with a self-signed cert/key'
        )
        parser.add_argument(
            '--dev-https', action='store_true', dest='dev_https', default=False,
            help=ahelp)

    def handle(self, *args, addrport=None, verbosity=1, dev_https, **kwargs):
        self.verbosity = verbosity
        os.environ['OTREE_USE_REDIS'] = '1'
        self.honcho = OTreeHonchoManager()
        self.setup_honcho(addrport=addrport, dev_https=dev_https)
        self.honcho.loop()
        sys.exit(self.honcho.returncode)

    def setup_honcho(self, *, addrport, dev_https):

        if addrport:
            m = re.match(naiveip_re, addrport)
            if m is None:
                raise CommandError('"%s" is not a valid port number '
                                   'or address:port pair.' % addrport)
            addr, _, _, _, port = m.groups()
        else:
            addr = None
            port = None

        addr = addr or DEFAULT_ADDR
        # Heroku uses $PORT
        port = int(port or os.environ.get('PORT') or DEFAULT_PORT)

        # https://github.com/encode/uvicorn/issues/185

        #asgi_server_cmd = f'uvicorn --host={addr} --port={port} --workers={NUM_WORKERS} otree_startup.asgi:application --log-level=debug'
        # keep-alive is needed, otherwise pages that take more than 5 seconds to load will trigger h13
        #asgi_server_cmd = f'hypercorn -b {addr}:{port} --workers={NUM_WORKERS} --keep-alive=35 otree_startup.asgi:application'
        asgi_server_cmd = f'daphne -b {addr} -p {port} otree_startup.asgi:application'

        if dev_https:
            raise SystemExit('--dev-https is currently under construction')
            # Because of HSTS, Chrome and other browsers will "get stuck" forcing HTTPS,
            # which makes it impossible to run regular devserver again on that port
            if int(port) == 8000:
                self.stderr.write('ERROR: oTree cannot use HTTPS on port 8000. Please specify a different port.')
                raise SystemExit(-1)
            # hypercorn format
            #asgi_server_cmd += ' --keyfile="{}" --certfile="{}"'.format(
            asgi_server_cmd += ' -e ssl:443:privateKey="{}":certKey="{}"'.format(
                get_ssl_file_path('development.key'),
                get_ssl_file_path('development.crt'),
            )
            # When the user submits AJAX such as AdvanceSlowest, Django gives REASON_BAD_REFERER.
            # because the referer is localhost:8003 and good_hosts just has 127.0.0.1.
            # could add localhost to CSRF_TRUSTED_ORIGINS, but that needs to be done
            # inside the asgi server process. i don't want to modify that setting globally
            # because that might have bad implications.
            # simplest workaround is to tell users to go to 127.0.0.1 instead of localhost.

        logger.info(asgi_server_cmd)

        honcho = self.honcho
        honcho.add_otree_process(
            'asgiserver',
            asgi_server_cmd
        )
