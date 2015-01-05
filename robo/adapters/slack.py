# -*- coding: utf-8 -*-
"""
    robo.adapters.slack
    ~~~~~~~~~~~~~~~~~~~

    Slack adapter.


    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import logging
from sleekxmpp import ClientXMPP

logger = logging.getLogger('robo')


class SlackXmpp(ClientXMPP):
    def __init__(self, jid, password, username, room):
        """Construct a xmpp client.

        :param jid: JID
        :param password: Slack password
        :param username: Bot name
        :param room: Chat room
        """
        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler('session_start', self.session_start)
        self.add_event_handler('message', self.receive)
        self.signal = None
        self.room = room
        self.nick = username

    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        self.plugin['xep_0045'].joinMUC(self.room, self.nick, wait=False)

    def muc_message(self, msg):
        if msg['mucnick'] != self.nick and self.nick in msg['body']:
            self.signal.send(msg['body'], original=msg, source='slack')


class Slack(object):
    def __init__(self, signal):
        logger.info('Start slack adapter.')
        password = os.environ['ROBO_SLACK_PASSWORD']
        room = os.environ['ROBO_SLACK_ROOM']
        team = os.environ['ROBO_SLACK_TEAM']
        username = os.environ['ROBO_SLACK_USERNAME']
        jid = '{0}@{1}.xmpp.slack.com'.format(username, team)
        logger.debug('jid is `{0}`.'.format(jid))
        logger.debug('room is `{0}`.'.format(room))

        self.xmpp = SlackXmpp(jid, password, username, room)
        self.xmpp.register_plugin('xep_0030')
        self.xmpp.register_plugin('xep_0045')
        self.xmpp.signal = signal

    def say(self, message, **kwargs):
        self.xmpp.send_message(mto=message.original['from'].bare,
                               mbody=message.body, mtype='groupchat')

    def run(self):
        if self.xmpp.connect():
            logging.info('Start xmpp client.')
            self.xmpp.process(block=True)
        else:
            logger.error('Cannot start xmpp client.')
