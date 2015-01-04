# -*- coding: utf-8 -*-
"""
    robo.handlers.ping
    ~~~~~~~~~~~~~~~~~~

    Ping.


    :copyright: (c) 2014 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from robo.decorators import cmd


class Ping(object):
    @cmd(regex=r'^ping$', description='Return PONG to PING')
    def say(self, message, **kwargs):
        return 'pong'
