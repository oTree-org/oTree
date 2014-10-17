#!/usr/bin/env python
"""
Simple wrapper around ./otree

This file exists to provide tools with a file called manage.py since services
like heroku expect the existence of such. As enduser you can and should always
use the ./otree script.
"""

import os
import sys
import subprocess


if __name__ == '__main__':
    base_path = os.path.dirname(os.path.abspath(__file__))
    otree_script = os.path.join(base_path, 'otree')

    return_code = subprocess.call([otree_script] + sys.argv[1:])
    sys.exit(return_code)
