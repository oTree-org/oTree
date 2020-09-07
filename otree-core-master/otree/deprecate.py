#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings


class OtreeDeprecationWarning(DeprecationWarning):
    pass


warnings.simplefilter('default', OtreeDeprecationWarning)
