#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six


class BaseConstantsMeta(type):

    def __setattr__(cls, attr, value):
        msg = "can't set attribute '{}'".format(attr)
        raise AttributeError(msg)


class BaseConstants(six.with_metaclass(BaseConstantsMeta, object)):

    pass
