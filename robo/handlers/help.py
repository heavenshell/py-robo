# -*- coding: utf-8 -*-
"""
    robo.handlers.help
    ~~~~~~~~~~~~~~~~~~

    Show registered handler's help.


    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from robo.decorators import cmd


class Help(object):
    @cmd(regex='^help$', description='Show this help message')
    def say(self, message, **kwargs):
        return '\n'.join(message.docs)
