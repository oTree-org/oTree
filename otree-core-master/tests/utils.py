#!/usr/bin/env python
# -*- coding: utf-8 -*-

import contextlib
import os
import shutil
import sys
import tempfile

from six import StringIO
from six.moves import urllib

from django.conf import settings
from django.core.management import call_command
from django.test.utils import override_settings

from otree.api import Page


class BlankTemplatePage(Page):
    template_name = 'global/BlankTemplatePage.html'


@contextlib.contextmanager
def add_path(path):
    """
    ::

        with add_path(new_sys_path):
            import strange_module
    """
    sys.path.insert(0, path)
    yield
    sys.path.pop(sys.path.index(path))


@contextlib.contextmanager
def capture_stdout(target=None):
    original = sys.stdout
    if target is None:
        target = StringIO()
    sys.stdout = target
    yield target
    target.seek(0)
    sys.stdout = original


@contextlib.contextmanager
def capture_stderr(target=None):
    original = sys.stderr
    if target is None:
        target = StringIO()
    sys.stderr = target
    yield target
    target.seek(0)
    sys.stderr = original


@contextlib.contextmanager
def cd(directory):
    """
    ::

        with cd(new_cwd):
            os.walk('.')
    """
    old_path = os.getcwd()
    os.chdir(directory)
    yield
    os.chdir(old_path)


@contextlib.contextmanager
def dummyapp(app):
    """
    Creates a new game app inside a temporary directory, adds this to the path
    and puts the app into the INSTALLED_APPS and INSTALLED_OTREE_APPS settings.

    It cleans the filesystem up afterwards.
    """
    tmpdir = tempfile.mkdtemp()
    app_path = os.path.join(tmpdir, app)

    os.mkdir(app_path)
    with capture_stdout():
        call_command('startapp', app, app_path)

    new_apps = list(settings.INSTALLED_APPS) + [app]
    new_otree_apps = list(settings.INSTALLED_OTREE_APPS) + [app]
    with add_path(tmpdir):
        with override_settings(
                INSTALLED_APPS=new_apps,
                INSTALLED_OTREE_APPS=new_otree_apps):
            yield app_path

        shutil.rmtree(tmpdir)
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)


def get_path(test_client_response, if_no_redirect):
    try:
        url = test_client_response.redirect_chain[-1][0]
    except IndexError:
        return if_no_redirect
    else:
        return urllib.parse.urlsplit(url).path
