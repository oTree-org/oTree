from django.core.management.commands import makemigrations
import six.moves

MIGRATIONS_WARNING = '''
oTree is not designed to be used with migrations. Instead, oTree uses the
'resetdb' command. You should only use 'makemigrations' and 'migrate'
if you understand how Django migrations work, and how to troubleshoot them.
'''


class Command(makemigrations.Command):

    def _confirm(self):
        self.stdout.write(MIGRATIONS_WARNING)
        answer = six.moves.input("Proceed? (y or n): ")
        if answer:
            return answer[0].lower() == 'y'
        return False

    def handle(self, *args, **options):

        if not self._confirm():
            self.stdout.write('Canceled.')
            return

        super(Command, self).handle(*args, **options)
