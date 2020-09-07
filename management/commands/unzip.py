from django.core.management.base import BaseCommand, CommandError
import tarfile
import logging
import os.path
import sys
from pathlib import Path
from django.conf import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Unzip a zipped oTree project"

    def add_arguments(self, parser):
        parser.add_argument(
            'zip_file', type=str, help="The .otreezip file")
        # it's good to require this arg because then it's obvious that the files
        # will be put in that subfolder, and not dumped in the current dir
        parser.add_argument(
            'output_folder', type=str, nargs='?',
            help="What to call the new project folder")

    def handle(self, **options):
        zip_file = options['zip_file']
        output_folder = options['output_folder'] or auto_named_output_folder(zip_file)
        unzip(zip_file, output_folder)
        msg = (
            f'Unzipped file. Enter this:\n'
            f'cd {esc_fn(output_folder)}\n'
        )

        logger.info(msg)


    def run_from_argv(self, argv):
        '''
        override this because the built-in django one executes system checks,
        which trips because settings are not configured.
        as at 2018-11-19, 'unzip' is the only
        otree-specific management command that doesn't require settings
        '''

        if len(argv) == 2:
            self.stdout.write(
                'You must provide the name of the *.otreezip file. Example:\n '
                'otree unzip AAA.otreezip'
            )
            sys.exit(-1)

        parser = self.create_parser(argv[0], argv[1])
        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        self.handle(**cmd_options)


def esc_fn(fn):
    if ' ' in fn:
        return f'\"{fn}\"'
    return fn

def auto_named_output_folder(zip_file_name) -> str:
    default_folder_name = Path(zip_file_name).stem

    if not Path(default_folder_name).exists():
        return default_folder_name

    logger.info(
        'Hint: you can provide the name of the folder to create. Example:\n'
        f"otree unzip {esc_fn(zip_file_name)} my_project"
    )
    for x in range(2, 20):
        folder_name = f'{default_folder_name}-{x}'
        if not Path(folder_name).exists():
            return folder_name
    logger.error(
        f"Could not unzip the file; target folder {folder_name} already exists. "
    )
    sys.exit(-1)


def unzip(zip_file: str, output_folder):
    if os.path.isfile('settings.py') and os.path.isfile('manage.py'):
        logger.error(
            'You are trying to unzip a project but it seems you are '
            'already in a project folder (found settings.py and manage.py).'
        )
        sys.exit(-1)

    with tarfile.open(zip_file) as tar:
        tar.extractall(output_folder)

