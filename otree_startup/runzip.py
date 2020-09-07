from typing import Optional
import logging
import os.path
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from otree.management.commands.unzip import unzip
import os.path
import os
import subprocess
import shutil
from time import sleep

logger = logging.getLogger(__name__)

# to make patching easy without modifying global sys.stdout.write which is essential
stdout_write = print


def main(remaining_argv):
    '''
    - top-level process that keeps checking for new files
    - subprocess is manage.py devserver
    - this is adapted from django autoreload
    '''
    try:
        if remaining_argv:
            [path] = remaining_argv
            exit_code = run_single_zipfile(path)
        else:
            exit_code = autoreload_for_new_zipfiles()
        # the rest is adapted from django autoreload, not sure why it's done
        # this way
        if exit_code < 0:
            os.kill(os.getpid(), -exit_code)
        else:
            sys.exit(exit_code)
    except KeyboardInterrupt:
        pass


def run_single_zipfile(fn: str) -> int:
    project = Project(Path(fn))
    project.unzip_to_tempdir()
    project.start()
    # from experimenting, this responds to Ctrl+C,
    # and there is no zombie subprocess
    return project.wait()


MSG_NO_OTREEZIP_YET = 'No *.otreezip file found in this folder yet, waiting...'
MSG_FOUND_NEWER_OTREEZIP = 'Newer project found'
MSG_RUNNING_OTREEZIP_NAME = "Running {}"

def autoreload_for_new_zipfiles() -> int:
    project = get_newest_project()
    newer_project = None
    if not project:
        stdout_write(MSG_NO_OTREEZIP_YET)
        while True:
            project = get_newest_project()
            if project:
                break
            sleep(1)

    tempdirs = []
    try:
        while True:
            if newer_project:
                project = newer_project
            stdout_write(MSG_RUNNING_OTREEZIP_NAME.format(project.zipname()))
            project.unzip_to_tempdir()
            if tempdirs:
                project.take_db_from_previous(tempdirs[-1].name)

            tempdirs.append(project.tmpdir)
            project.start()
            try:
                while True:
                    # if process is still running, poll() returns None
                    exit_code = project.poll()
                    if exit_code != None:
                        return exit_code
                    sleep(1)
                    latest_project = get_newest_project()
                    # it's possible that zipfile was deleted while the program
                    # was running
                    if latest_project and latest_project.mtime() > project.mtime():
                        newer_project = latest_project
                        # use stdout.write because logger is not configured
                        # (django setup has not even been run)
                        stdout_write(MSG_FOUND_NEWER_OTREEZIP)
                        break
            finally:
                project.terminate()
    finally:
        for td in tempdirs:
            td.cleanup()


class Project:
    tmpdir: TemporaryDirectory = None
    _proc: subprocess.Popen

    def __init__(self, otreezip: Path):
        self._otreezip = otreezip

    def zipname(self):
        return self._otreezip.name

    def mtime(self):
        return self._otreezip.stat().st_mtime

    def unzip_to_tempdir(self):
        self.tmpdir = TemporaryDirectory()
        unzip(str(self._otreezip), self.tmpdir.name)

    def start(self):
        self._proc = subprocess.Popen(
            [sys.executable, 'manage.py', 'devserver', '--noreload', '--inside-runzip'],
            cwd=self.tmpdir.name,
            env=os.environ.copy(),
        )

    def delete_otreezip(self):
        self._otreezip.unlink()

    def poll(self):
        return self._proc.poll()

    def terminate(self):
        return self._proc.terminate()

    def wait(self) -> int:
        return self._proc.wait()

    def take_db_from_previous(self, other_tmpdir: str):
        for item in ['__temp_migrations', 'db.sqlite3']:
            item_path = Path(other_tmpdir) / item
            if item_path.exists():
                shutil.move(str(item_path), self.tmpdir.name)


MAX_OTREEZIP_FILES = 10
MSG_DELETING_OLD_OTREEZIP = 'Deleting old file: {}'

# returning the time together with object makes it easier to test
def get_newest_project() -> Optional[Project]:

    projects = [Project(path) for path in Path('.').glob('*.otreezip')]
    if not projects:
        return None

    sorted_projects = sorted(projects, key=lambda proj: proj.mtime(), reverse=True)
    newest_project = sorted_projects[0]

    # cleanup so they don't end up with hundreds of zipfiles
    for old_proj in sorted_projects[MAX_OTREEZIP_FILES:]:
        stdout_write(MSG_DELETING_OLD_OTREEZIP.format(old_proj.zipname()))
        old_proj.delete_otreezip()

    return newest_project

