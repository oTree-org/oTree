from channels.management.commands import runserver
import otree.bots.browser
from django.conf import settings
import otree.common_internal
import logging
from daphne.endpoints import build_endpoint_description_strings
import otree_startup
import os


class Command(runserver.Command):

    def handle(self, *args, **options):

        self.verbosity = options.get("verbosity", 1)

        from otree.common_internal import release_any_stale_locks
        release_any_stale_locks()

        # for performance,
        # only run checks when the server starts, not when it reloads
        # (RUN_MAIN is set by Django autoreloader).
        if not os.environ.get('RUN_MAIN'):

            try:
                # don't suppress output. it's good to know that check is
                # not failing silently or not being run.
                # also, intercepting stdout doesn't even seem to work here.
                self.check(display_num_errors=True)

            except Exception as exc:
                otree_startup.print_colored_traceback_and_exit(exc)

        super().handle(*args, **options)

    def inner_run(self, *args, **options):

        '''
        inner_run does not get run twice with runserver, unlike .handle()
        '''

        # initialize browser bot worker in process memory
        otree.bots.browser.browser_bot_worker = otree.bots.browser.Worker()

        addr = f'[{self.addr}]' if self._raw_ipv6 else self.addr
        # 0.0.0.0 is not a regular IP address, so we can't tell the user
        # to open their browser to that address
        if addr == '127.0.0.1':
            addr = 'localhost'
        elif addr == '0.0.0.0':
            addr = '<ip_address>'
        self.stdout.write((
            "Starting server.\n"
            "Open your browser to http://%(addr)s:%(port)s/\n"
            "To quit the server, press Control+C.\n"
        ) % {
            "addr": addr,
            "port": self.port,
        })

        # silence the lines like:
        # 2018-01-10 18:51:18,092 - INFO - worker - Listening on channels
        # http.request, otree.create_session, websocket.connect,
        # websocket.disconnect, websocket.receive
        daphne_logger = logging.getLogger('django.channels')
        original_log_level = daphne_logger.level
        daphne_logger.level = logging.WARNING

        endpoints = build_endpoint_description_strings(host=self.addr, port=self.port)
        application = self.get_application(options)

        # silence the lines like:
        # INFO HTTP/2 support not enabled (install the http2 and tls Twisted extras)
        # INFO Configuring endpoint tcp:port=8000:interface=127.0.0.1
        # INFO Listening on TCP address 127.0.0.1:8000
        logging.getLogger('daphne.server').level = logging.WARNING

        try:
            self.server_cls(
                application=application,
                endpoints=endpoints,
                signal_handlers=not options["use_reloader"],
                action_logger=self.log_action,
                http_timeout=self.http_timeout,
                root_path=getattr(settings, "FORCE_SCRIPT_NAME", "") or "",
                websocket_handshake_timeout=self.websocket_handshake_timeout,
            ).run()
            daphne_logger.debug("Daphne exited")
        except KeyboardInterrupt:
            shutdown_message = options.get("shutdown_message", "")
            if shutdown_message:
                self.stdout.write(shutdown_message)
            return


    def add_arguments(self, parser):
        super().add_arguments(parser)
        # see log_action below; we only show logs of each request
        # if verbosity >= 1.
        # this still allows logger.info and logger.warning to be shown.
        # NOTE: if we change this back to 1, then need to update devserver
        # not to show traceback of errors.
        parser.set_defaults(verbosity=0)

    def log_action(self, protocol, action, details):
        '''
        Override log_action method.
        Need this until https://github.com/django/channels/issues/612
        is fixed.
        maybe for some minimal output use this?
            self.stderr.write('.', ending='')
        so that you can see that the server is running
        (useful if you are accidentally running multiple servers)

        idea: maybe only show details if it's a 4xx or 5xx.

        '''
        if self.verbosity >= 1:
            super().log_action(protocol, action, details)
