#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa

from django.forms import *

# Delete `fields` and `widgets` attributes which came from Django and
# would otherwise make it impossible to import e.g. the otree.forms.fields
# module.
del fields
del widgets

from .fields import *
from .forms import *
from .widgets import *
