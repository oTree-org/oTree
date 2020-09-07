#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa

# Keep backwards compatibility with older otree's
# We moved the otree.widgets module to otree.forms.widgets
# prior to adding otree.api in 2016, each models.py contained:
# "from otree import widgets"

from .forms.widgets import *
