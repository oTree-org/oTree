#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import warnings

import otree
from otree.deprecate import OtreeDeprecationWarning


procfile_path = os.path.join(
    os.path.dirname(otree.__file__), 'project_template', 'Procfile')

with open(procfile_path, 'r') as procfile:
    procfile_contents = procfile.read()


DEPRECATION_STRING = '''
oTree is using a new server. You should start it with a different command.
In your project's root directory, find the file called 'Procfile',
and change its contents to the following:

{}

If using Heroku, you should also install the Heroku Redis add-on,
then run "heroku restart".

More information here: http://otree.readthedocs.io/en/latest/v0.5.html
'''.format(procfile_contents)


warnings.warn(DEPRECATION_STRING, OtreeDeprecationWarning)


def application(environ, start_response):
    data = DEPRECATION_STRING.encode('utf-8')
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    return iter([data])
