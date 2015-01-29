#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from otree.management.cli import execute_from_command_line
    execute_from_command_line(sys.argv, script_file=__file__)
