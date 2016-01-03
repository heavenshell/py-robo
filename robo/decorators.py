# -*- coding: utf-8 -*-
""" robo.decorators
    ~~~~~~~~~~~~~~~

    Decorators.


    :copyright: (c) 2016 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from functools import wraps


def cmd(*args, **kwargs):
    def _cmd(f):
        f.__robo_event = True
        f.__robo_kwargs = kwargs

        @wraps(f)
        def __cmd(func, message, **_kwargs):
            return f(func, message, **_kwargs)

        return __cmd

    return _cmd
