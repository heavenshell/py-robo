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
        description_length = 0
        for d in message.docs:
            if len(d['description']) > description_length:
                description_length = len(d['description'])

        msg = 'Description: {0:%s} Pattern: {1}' % description_length
        docs = []
        for doc in message.docs:
            docs.append(msg.format(doc['description'], doc['pattern']))

        return '\n'.join(docs)
