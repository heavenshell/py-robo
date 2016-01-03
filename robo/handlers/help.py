# -*- coding: utf-8 -*-
"""
    robo.handlers.help
    ~~~~~~~~~~~~~~~~~~

    Show registered handler's help.


    :copyright: (c) 2016 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from robo.decorators import cmd


class Help(object):
    @cmd(regex='^help$', description='Show this help message')
    def say(self, message, **kwargs):
        pattern_length = 0
        for d in message.docs:
            if len(d['pattern']) > pattern_length:
                pattern_length = len(d['pattern'])

        msg = '{0} {1:%s} - {2}' % pattern_length
        docs = []
        for doc in message.docs:
            description = msg.format(doc['robot_name'], doc['pattern'],
                                     doc['description'])
            docs.append(description)

        return '\n'.join(docs)
