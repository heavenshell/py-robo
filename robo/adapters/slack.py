# -*- coding: utf-8 -*-
"""
    robo.adapters.slack
    ~~~~~~~~~~~~~~~~~~~

    Slack adapter.


    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
from sleekxmpp import ClientXMPP


class SlackXmpp(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler('session_start', self.session_start)
        self.add_event_handler('message', self.receive)
        self.signal = None

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

    def receive(self, msg):
        self.signal.send(msg.body, original=msg, source='slack')


class Slack(object):
    def __init__(self, signal):
        password = os.environ['ROBO_SLACK_PASSWORD']
        room = os.environ['ROBO_SLACK_ROOM']
        team = os.environ['ROBO_SLACK_TEAM']
        username = os.environ['ROBO_SLACK_USERNAME']
        jid = '{0}@{1}.xmpp.slack.com'.format(username, team)

        self.xmpp = SlackXmpp(jid, password)
        self.xmpp.signal = signal

    def say(self, message, **kwargs):
        message.original.reply(message.body).send()

    def run(self):
        pass
