import os
from django.core.management.commands import startproject
from django.core.management.base import CommandError
import sys
import otree



class Command(startproject.Command):
    help = ("Creates a new oTree project.")

    def add_arguments(self, parser):
        super().add_arguments(parser)
        '''need this so we can test startproject automatically'''
        parser.add_argument(
            '--noinput', action='store_false', dest='interactive',
            default=True)

    def handle(self, *args, **options):
        project_name = options['name']
        if os.path.isfile('settings.py') and os.path.isfile('manage.py'):
            self.stdout.write(
                'You are trying to create a project but it seems you are '
                'already in a project folder (found settings.py and manage.py).'
            )
            sys.exit(-1)
        if os.path.exists(project_name):
            msg = (
                f'It appears you already created a project called "{project_name}" '
                'in this folder. Either delete that folder first, or use a different name.'
            )
            self.stdout.write(msg)
            sys.exit(-1)

        if options['interactive']:
            answer = input("Include sample games? (y or n): ")
        else:
            answer = 'n'
        if answer and answer[0].lower() == "y":
            project_template_path = (
                "https://github.com/oTree-org/oTree/archive/master.zip")
        else:
            project_template_path = os.path.join(
                os.path.dirname(otree.__file__), 'project_template')

        options['template'] = project_template_path

        try:
            super().handle(*args, **options)
        except CommandError as exc:
            # Django startproject first creates an empty folder and then tries to
            # download the project template, etc. If an error occurs, the empty project
            # folder is not deleted, which can confuse people.
            # this will not delete any files created by the user because we
            # would have caught that above when we checked if the folder existed.
            if os.path.exists(project_name):
                os.rmdir(project_name)

            is_macos = sys.platform.startswith('darwin')
            if is_macos and 'CERTIFICATE_VERIFY_FAILED' in str(exc):
                py_major, py_minor = sys.version_info[:2]
                msg = (
                    'CERTIFICATE_VERIFY_FAILED: '
                    'Before downloading the sample games, '
                    'you need to install SSL certificates. '
                    'Usually this can be resolved by entering this command:\n'
                    '/Applications/Python\\ {}.{}/Install\\ Certificates.command'
                ).format(py_major, py_minor)
                self.stdout.write(msg)
                sys.exit(-1)
            raise
        # this assumes the 'directory' arg was unused, which will be true
        # for 99% of oTree users.
        msg = (
            'Created project folder.\n'
            'Enter "cd {}" to move inside the project folder, '
            'then start the server with "otree devserver".' #
        ).format(project_name)
        self.stdout.write(msg)
