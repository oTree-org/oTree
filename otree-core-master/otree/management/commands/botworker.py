import logging
from django.core.management.base import BaseCommand
import otree.bots.browser
from otree.common_internal import get_redis_conn


# =============================================================================
# LOGGING
# =============================================================================

logger = logging.getLogger('otree.botworker')


# =============================================================================
# COMMAND
# =============================================================================

class Command(BaseCommand):
    help = "oTree: Run the worker for browser bots."

    def handle(self, *args, **options):
        redis_conn = get_redis_conn()
        otree.bots.browser.redis_flush_bots(redis_conn)
        worker = otree.bots.browser.Worker(redis_conn)
        worker.redis_listen()
