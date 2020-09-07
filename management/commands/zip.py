'''
Even though this command doesn't require Django to be setup,
it should run after django.setup() just to make sure it doesn't
crash when pushed to Heroku
'''

from django.core.management.base import BaseCommand
import tarfile
import os
import logging
from pathlib import Path
import sys
import re

logger = logging.getLogger(__name__)

# need to resolve to expand path
PROJECT_PATH = Path('.').resolve()

# don't want to use the .gitignore format, it looks like a mini-language
# https://git-scm.com/docs/gitignore#_pattern_format

# TODO: maybe some of these extensions like .env, staticfiles could legitimately exist in subfolders.
EXCLUDED_PATH_ENDINGS = '~ .git db.sqlite3 .pyo .pyc .pyd .idea .DS_Store .otreezip venv _static_root staticfiles __pycache__ .env'.split()


# TODO: make sure we recognize and exclude virtualenvs, even if not called venv

def filter_func(tar_info: tarfile.TarInfo):

    path = tar_info.path

    for ending in EXCLUDED_PATH_ENDINGS:
        if path.endswith(ending):
            return None

    if '__temp' in path:
        return None

    # size is in bytes
    kb = tar_info.size >> 10
    if kb > 500:
        logger.info(f'Adding large file ({kb} KB): {path}')

    # make sure all dirs are writable, so their children can be deleted,
    # so that otree unzip/runzip work as expected.
    # we were getting some folders with permission 16749.
    tar_info.mode |= 0o222
    return tar_info


class Command(BaseCommand):
    help = "Zip into an archive"

    def handle(self, **options):
        # remove these lines after a month or so
        legacy_filename = 'zipped.otreezip'
        if os.path.exists(legacy_filename):
            self.stdout.write('removing zipped.otreezip, this should only happen once')
            os.remove(legacy_filename)
        zip_project(PROJECT_PATH)

    def run_from_argv(self, argv):
        '''
        copy-pasted from 'unzip' command
        '''

        parser = self.create_parser(argv[0], argv[1])
        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        self.handle(**cmd_options)


def zip_project(project_path: Path):
    # always use the same name for simplicity and so that we don't get bloat
    # or even worse, all the previous zips being included in this one
    # call it zipped.tar so that it shows up alphabetically last
    # (using __temp prefix makes it show up in the middle, because it's a file)
    archive_name = f'{project_path.name}.otreezip'

    settings_file = project_path / 'settings.py'
    if not settings_file.exists():
        msg = (
            "Cannot find oTree settings. "
            "You must run this command from the folder that contains your "
            "settings.py file."
        )
        logger.error(msg)
        sys.exit(1)

    try:
        check_requirements_files(project_path)
    except RequirementsError as exc:
        logger.error(str(exc))
        sys.exit(1)

    # once Heroku uses py 3.7 by default, we can remove this runtime stuff.
    runtime_txt = project_path / 'runtime.txt'
    runtime_existed = runtime_txt.exists()
    if not runtime_existed:
        # don't use sys.version_info because it might be newer than what
        # heroku supports
        runtime_txt.write_text(f'python-3.7.3')
    try:
        with tarfile.open(archive_name, 'w:gz') as tar:
            # if i omit arcname, it nests the project 2 levels deep.
            # if i say arcname=proj, it puts the whole project in a folder.
            # if i say arcname='', it has 0 levels of nesting.
            tar.add(project_path, arcname='', filter=filter_func)
    finally:
        if not runtime_existed:
            runtime_txt.unlink()
    logger.info(f'Saved your code into file "{archive_name}"')


def get_non_comment_lines(f):
    lines = []
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            lines.append(line)
    return lines


class RequirementsError(Exception): pass


def check_requirements_files(project_path: Path):
    reqs_server_path = project_path / 'requirements_server.txt'
    if reqs_server_path.exists():
        # checking legacy requirements structure is too complicated,
        # skip it.
        return

    reqs_path = project_path / 'requirements.txt'
    reqs_base_path = project_path / 'requirements_base.txt'
    reqs_base_exists = reqs_base_path.exists()

    if not reqs_path.exists():
        raise RequirementsError(
            "You need a requirements.txt in your project folder"
        )

    with reqs_path.open() as f:
        all_req_lines = get_non_comment_lines(f)

    reqs_base_should_exist = False
    for ln in all_req_lines:
        if 'requirements_base.txt' in ln:
            reqs_base_should_exist = True

    if reqs_base_exists != reqs_base_should_exist:
        if reqs_base_should_exist:
            raise RequirementsError(
                'Your requirements.txt calls requirements_base.txt, '
                'but requirements_base.txt was not found.'
            )
        else:
            raise RequirementsError(
                'Your requirements_base.txt '
                'is being ignored. '
                'Add the following line to requirements.txt:\n'
                '-r requirements_base.txt'
            )

    if reqs_base_exists:
        with reqs_base_path.open() as f:
            all_req_lines.extend(get_non_comment_lines(f))

    psycopg2_found = False
    for ln in all_req_lines:
        if 'psycopg2' in ln:
            psycopg2_found = True

    if not psycopg2_found:
        raise RequirementsError(
            'Your requirements.txt must have a line that says "psycopg2", '
            'which is necessary for Postgres. '
        )

    # check duplicates
    already_seen = set()
    for ln in all_req_lines:

        m = re.match(
            '(^[\w-]+).*?',
            ln)
        if m:
            package = m.group(1)
            if package in already_seen:
                if reqs_base_exists:
                    raise RequirementsError(
                        f'"{package}" is listed more than once '
                        'in your requirements_base.txt and/or requirements.txt. '
                    )
                else:
                    raise RequirementsError(
                        f'"{package}" is listed more than once '
                        'in your requirements.txt. '
                    )
            already_seen.add(package)