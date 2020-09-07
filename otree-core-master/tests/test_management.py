#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock

from six import StringIO

from django.core.management import call_command

from otree.management import cli
from otree.deprecate import OtreeDeprecationWarning

from .base import TestCase


class CeleryCommand(TestCase):

    def test_handle(self):
        self.assertWarns(OtreeDeprecationWarning,
                         lambda: call_command("celery"))


class OTreeAndDjangoVersion(TestCase):

    @mock.patch("otree.get_version", return_value="foo")
    @mock.patch("django.get_version", return_value="faa")
    def test_otree_and_django_version(self, dget_version, oget_version):
        actual = cli.otree_and_django_version()
        expected = 'oTree: foo - Django: faa'

        self.assertTrue(dget_version.called)
        self.assertTrue(oget_version.called)
        self.assertEqual(actual, expected)


class OTreeManagementUtility(TestCase):

    @mock.patch("sys.argv", new=["otree", "--help"])
    @mock.patch("platform.system", return_value="No-Windows")
    def test_help(self, *args):
        arguments = ["otree", "--help"]

        expected = StringIO()
        with mock.patch("sys.stdout", new=expected):
            cli.execute_from_command_line(arguments, "otree")

        utility = cli.OTreeManagementUtility(arguments)
        actual = StringIO()
        with mock.patch("sys.stdout", new=actual):
            utility.execute()

        self.assertEquals(actual.getvalue(), expected.getvalue())

    def test_commands_only(self, *args):
        utility = cli.OTreeManagementUtility([])
        main_help_text = utility.main_help_text().splitlines()
        for command in utility.main_help_text(commands_only=True).splitlines():
            prefix = "  {} - ".format(command)
            found = False
            for line in main_help_text:
                if line.startswith(prefix):
                    found = True
                    break
            if not found:
                self.fail("Command '{}' no found in help".format(command))

    def test_settings_exception(self):
        expected = ('Note that only Django core commands are listed as '
                    'settings are not properly configured (error: foo).')

        utility = cli.OTreeManagementUtility([])
        utility.settings_exception = "foo"
        main_help_text = utility.main_help_text().splitlines()

        self.assertEquals(main_help_text[-1], expected)

        utility = cli.OTreeManagementUtility([])
        utility.settings_exception = None
        main_help_text = utility.main_help_text().splitlines()

        self.assertNotEquals(main_help_text[-1], expected)


class ExecuteFromCommandLine(TestCase):

    @mock.patch("platform.system", return_value="No-Windows")
    @mock.patch("otree.management.cli.OTreeManagementUtility")
    def test_execute_from_command_line_runserver(self, *args):
        management, system = args
        cli.execute_from_command_line(["otree", "runserver"], "script.py")
        management.assert_called_with(["otree", "runserver"])

    # not working at the moment because of SSL server
    '''
    @mock.patch("platform.system", return_value="No-Windows")
    @mock.patch("otree.management.cli.OTreeManagementUtility")
    @mock.patch("django.conf.LazySettings.AWS_ACCESS_KEY_ID", create=True)
    def test_execute_from_command_line_runserver_ssh(self, *args):
        key, management, system = args
        cli.execute_from_command_line(["otree", "runserver"], "script.py")
        management.assert_called_with(["otree", "runsslserver"])
    '''

    # not working at the moment because of pypi cli check
    '''
    @mock.patch("platform.system", return_value="No-Windows")
    @mock.patch("sys.stdout")
    @mock.patch("otree.management.cli.otree_and_django_version",
                return_value="foo")
    def test_execute_from_command_line_runserver_no_env_command(self, *args):
        version, stdout, system = args
        cli.execute_from_command_line(["version"], "script.py")
        self.assertTrue(version.called)
        stdout.write.assert_called_with("foo\n")
    '''


class OTreeCli(TestCase):

    @mock.patch("sys.stdout")
    @mock.patch("sys.stderr")
    @mock.patch("sys.argv", new=["otree", "runserver"])
    def test_import_settings_fail(self, *args):
        settings_patch = mock.patch(
            "otree.management.cli.settings",
            create=True)
        with settings_patch as settings:
            type(settings).INSTALLED_APPS = mock.PropertyMock(
                side_effect=ImportError)
            with self.assertRaises(SystemExit):
                cli.otree_cli()

    @mock.patch("sys.argv", new=["--help"])
    @mock.patch("otree.management.cli.execute_from_command_line")
    def test_clean_run(self, execute_from_command_line):
        cli.otree_cli()
        execute_from_command_line.assert_called_with(["--help"], 'otree')

    @mock.patch("sys.argv", new=["--version"])
    @mock.patch("otree.management.cli.execute_from_command_line")
    @mock.patch("os.getcwd", return_value="foo")
    def test_add_pwd(self, *args):
        gcwd, execute_from_command_line = args
        with mock.patch("sys.path", new=[]) as path:
            cli.otree_cli()
            self.assertEquals(path, ["foo"])
        self.assertTrue(gcwd.called)
        execute_from_command_line.assert_called_with(["--version"], 'otree')
