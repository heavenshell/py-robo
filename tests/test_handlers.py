# -*- coding: utf-8 -*-
"""
    robo.tests.test_handlers
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Builtin handlers test.


    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import re
from functools import partial
from unittest import TestCase
from robo.robot import Robot
from robo.message import Message
from robo.handlers.echo import Echo
from robo.handlers.ping import Ping
from robo.handlers.help import Help


def create_robot():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    get_path = partial(os.path.join, here)
    handler_path = get_path('robo/handlers')
    adapter_path = get_path('tests/fixtures/adapters')
    robot = Robot()
    robot.setup_handlers(handler_path)
    robot.setup_adapters(adapter_path, 'null',
                         package='tests.fixtures.adapters')

    return robot


class TestEchoHandlers(TestCase):
    def test_should_response_repete_command(self):
        """ Echo().say() should repeat command. """
        regex = re.compile(r'echo\s+(.*)')
        match = regex.match('echo hello')

        ret = Echo().say(Message(body='echo hello', match=match))
        self.assertEqual(ret, 'hello')

    def test_should_response_repete_command_by_sending_signal(self):
        """ Handler should repeat command when signal send. """
        robot = create_robot()
        robot.handler_signal.send('robo echo hello')
        ret = robot.adapters['null'].responses[0]
        self.assertEqual(ret, 'hello')


class TestPingHandler(TestCase):
    def test_should_response_pong(self):
        """ Ping().say() should response pong. """
        ret = Ping().say(Message(body='ping', match=None))
        self.assertEqual(ret, 'pong')

    def test_should_response_pong_by_sending_signal(self):
        """ Handler should repeat command when signal send. """
        robot = create_robot()
        robot.handler_signal.send('robo ping')
        ret = robot.adapters['null'].responses[0]
        self.assertEqual(ret, 'pong')


class TestHelpHandler(TestCase):
    def test_should_response_all_help(self):
        """ Help().say() should response all help. """
        robot = create_robot()
        ret = Help().say(Message(body='', docs=robot.docs, match=None))
        expected = [
            'Description: Repeate your command   Pattern: echo\s+(.*)',
            'Description: Show this help message Pattern: ^help$',
            'Description: Return PONG to PING    Pattern: ^ping$'
        ]
        self.assertEqual(ret, '\n'.join(expected))

    def test_should_response_help_by_sending_signal(self):
        """ Handler should show help when signal send. """
        robot = create_robot()
        robot.handler_signal.send('robo help')
        ret = robot.adapters['null'].responses[0]
        expected = [
            'Description: Repeate your command   Pattern: echo\s+(.*)',
            'Description: Show this help message Pattern: ^help$',
            'Description: Return PONG to PING    Pattern: ^ping$'
        ]
        self.assertEqual(ret, '\n'.join(expected))
