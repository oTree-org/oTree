# make Django's native 'test' command available to those who need it
# because oTree overrides it.

from django.core.management.commands.test import Command # noqa