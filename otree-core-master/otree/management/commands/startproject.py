#!/usr/bin/env python
# -*- coding: utf-8 -*-


# =============================================================================
# IMPORTS
# =============================================================================

import sys
import os
import platform
import shutil

from django.core.management.commands import startproject

import six

import otree
from otree.common_internal import (
    pypi_updates_cli, add_empty_migrations_to_all_apps)


# =============================================================================
# CONSTANTS
# =============================================================================

IMPLEMENTATIONS_ALIAS = {
    "CPython": "python"
}


# =============================================================================
# COMMAND
# =============================================================================

class Command(startproject.Command):
    help = ("Creates a new oTree project.")

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        ahelp = (
            'Tells the command to NOT prompt the user for '
            'input of any kind.')
        parser.add_argument(
            '--noinput', action='store_false', dest='interactive',
            default=True, help=ahelp)

    def modify_project_files(self, options):
        project_name, target = options['name'], options['directory']
        if target is None:
            project_root_dir = os.path.join(os.getcwd(), project_name)
        else:
            project_root_dir = os.path.abspath(os.path.expanduser(target))

        imp = platform.python_implementation()
        implementation_name = IMPLEMENTATIONS_ALIAS.get(imp, imp).lower()
        version = ".".join(map(str, sys.version_info[:3]))
        runtime_string = "{}-{}\n".format(implementation_name, version)

        runtime_path = os.path.join(project_root_dir, "runtime.txt")
        with open(runtime_path, "w") as fp:
            fp.write(runtime_string)

        # overwrite Procfile with new channels/asgi one
        procfile_path = os.path.join(
            self.core_project_template_path, 'Procfile')
        shutil.copy(procfile_path, project_root_dir)

        # migrations
        add_empty_migrations_to_all_apps(project_root_dir)

    def handle(self, *args, **options):
        if options["interactive"]:
            answer = None
            while not answer or answer not in "yn":
                answer = six.moves.input("Include sample games? (y or n): ")
                if not answer:
                    answer = "y"
                    break
                else:
                    answer = answer[0].lower()
        else:
            answer = 'n'
        self.core_project_template_path = os.path.join(
                os.path.dirname(otree.__file__), 'project_template')
        if answer == "y":
            project_template_path = (
                "https://github.com/oTree-org/oTree/archive/master.zip")
        else:
            project_template_path = self.core_project_template_path
        if options.get('template', None) is None:
            options['template'] = project_template_path
        super(Command, self).handle(*args, **options)

        self.modify_project_files(options)
        try:
            pypi_updates_cli()
        except:
            pass
        print('Created project folder.')
