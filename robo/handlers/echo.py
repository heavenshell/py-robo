# -*- coding: utf-8 -*-
"""
    robo.handlers.echo
    ~~~~~~~~~~~~~~~~~~

    Echo.


    :copyright: (c) 2016 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from robo.decorators import cmd


class Echo(object):
    @cmd(regex=r'echo\s+(.*)', description='Repeate your command')
    def say(self, message, **kwargs):
        return message.match.group(1)
