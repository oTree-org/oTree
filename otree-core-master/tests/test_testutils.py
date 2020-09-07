import os
import sys
import tempfile

from .base import TestCase
from .utils import add_path, capture_stdout, cd


class AddPathTest(TestCase):
    def test_add_path(self):
        tmpdir = tempfile.mkdtemp()
        original_path = sys.path[:]
        with add_path(tmpdir):
            self.assertEqual(len(sys.path), len(original_path) + 1)
            self.assertTrue(tmpdir in sys.path)
        self.assertEqual(sys.path, original_path)
        self.assertTrue(tmpdir not in sys.path)


class CaptureStdoutTest(TestCase):
    def test_capture(self):
        with capture_stdout() as output:
            print("Hello world!")
        self.assertEqual(output.read(), "Hello world!\n")

    def test_stdout_chagned(self):
        original_stdout = sys.stdout
        self.assertTrue(sys.stdout is original_stdout)
        with capture_stdout():
            self.assertFalse(sys.stdout is original_stdout)
        self.assertTrue(sys.stdout is original_stdout)


class CdTest(TestCase):
    def test_cd(self):
        tmpdir = tempfile.mkdtemp()
        # OS X returns symlinks for the temporary directory.
        # We need to resolve to the real path in order to reliably test the
        # outcome of a os.chdir()
        # See: http://stackoverflow.com/q/12482702/199848
        tmpdir = os.path.realpath(tmpdir)

        current_cwd = os.getcwd()
        self.assertEqual(os.getcwd(), current_cwd)
        with cd(tmpdir):
            self.assertEqual(os.getcwd(), tmpdir)
        self.assertEqual(os.getcwd(), current_cwd)

    def test_cd_with_cwd(self):
        current_cwd = os.getcwd()
        self.assertEqual(os.getcwd(), current_cwd)
        with cd(current_cwd):
            self.assertEqual(os.getcwd(), current_cwd)
        self.assertEqual(os.getcwd(), current_cwd)
