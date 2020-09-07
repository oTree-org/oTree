import os
import shutil
import tempfile

from django.core.management import call_command

from .base import TestCase
from .utils import capture_stdout, cd


class StartProjectTest(TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        print('tmp_dir:', self.tmp_dir)

    def tearDown(self):
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

    def test_call_startproject(self):
        with cd(self.tmp_dir), capture_stdout():
            call_command('startproject', 'newproj', '--noinput')

        path = os.path.join(self.tmp_dir, 'newproj')
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.isdir(path))
        self.assertTrue(os.path.exists(os.path.join(path, 'settings.py')))
