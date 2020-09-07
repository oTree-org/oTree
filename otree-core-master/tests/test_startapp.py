import os
import shutil
import tempfile

from django.conf import settings
from django.core.management import call_command, CommandError

from mock import patch

import otree.checks
from .base import TestCase
from .utils import add_path, capture_stdout, cd


class StartAppTest(TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

    def test_call_startapp(self):
        with cd(self.tmp_dir), capture_stdout():
            call_command('startapp', 'newgame')

        path = os.path.join(self.tmp_dir, 'newgame')
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.isdir(path))
        self.assertTrue(os.path.exists(os.path.join(path, 'models.py')))

    def test_call_startapp_with_destination(self):
        path = os.path.join(self.tmp_dir, 'anothergame')
        os.mkdir(path)

        with capture_stdout():
            call_command('startapp', 'anothergame', path)

        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.isdir(path))
        self.assertTrue(os.path.exists(os.path.join(path, 'models.py')))

    def test_startapp_passes_system_check(self):
        app_path = os.path.join(self.tmp_dir, 'tobecheckedgame')
        with cd(self.tmp_dir), capture_stdout():
            call_command('startapp', 'tobecheckedgame')

        new_apps = list(settings.INSTALLED_APPS)
        new_otree_apps = list(settings.INSTALLED_OTREE_APPS)
        new_apps.append('tobecheckedgame')
        new_otree_apps.append('tobecheckedgame')

        with add_path(self.tmp_dir):
            with self.settings(
                    INSTALLED_APPS=new_apps,
                    INSTALLED_OTREE_APPS=new_otree_apps):

                # This check should pass successfully.
                with capture_stdout():
                    call_command('check')

                # Now make sure that check was actually performed by breaking
                # things.

                # Removing views.py which should cause the checks to fail
                os.unlink(os.path.join(app_path, 'views.py'))

                def run_check():
                        with capture_stdout():
                            call_command('check')

                self.assertRaises(CommandError, run_check)

    def test_startapp_is_checked_with_system_check(self):
        # Gather some data how often the file_exists check is executed. That
        # way we can compare it later to make sure that the new app was tested
        # as well.
        with patch.object(otree.checks.Rules, 'file_exists') as file_exists:
            file_exists.return_value = True
            with capture_stdout():
                call_command('check')
            self.assertTrue(file_exists.called)

        with cd(self.tmp_dir):
            with capture_stdout():
                call_command('startapp', 'brokengame')

        new_apps = list(settings.INSTALLED_APPS)
        new_otree_apps = list(settings.INSTALLED_OTREE_APPS)
        new_apps.append('brokengame')
        new_otree_apps.append('brokengame')

        with add_path(self.tmp_dir):
            with self.settings(
                INSTALLED_APPS=new_apps, INSTALLED_OTREE_APPS=new_otree_apps
            ):
                with patch.object(otree.checks.Rules, 'file_exists') as fexist:
                    fexist.return_value = True
                    with capture_stdout():
                        call_command('check')
                    self.assertTrue(fexist.called)
