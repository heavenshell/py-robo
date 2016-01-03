# -*- coding: utf-8 -*-
"""
    robo.adapters.shell
    ~~~~~~~~~~~~~~~~~~~

    Shell.


    :copyright: (c) 2016 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import sys
import code
import logging


class Console(code.InteractiveConsole):
    def __init__(self, local=None, filename='<console>'):
        code.InteractiveConsole.__init__(self, local, filename)
        self.signal = None

    def push(self, line):
        self.signal.send(line, source='shell')


class Shell(object):
    def __init__(self, signal):
        self.console = Console()
        self.console.signal = signal

        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(fmt='%(message)s'))
        logger = logging.getLogger('robo.adapters.shell')
        logger.propagate = False
        logger.addHandler(handler)
        self.logger = logger

    def say(self, message, **kwargs):
        self.logger.info(message)

    def run(self):
        sys.ps1 = '> '
        self.console.interact('^D to exit.')
