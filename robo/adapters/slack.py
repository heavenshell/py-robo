# -*- coding: utf-8 -*-
"""
    robo.adapters.slack
    ~~~~~~~~~~~~~~~~~~~

    Slack adapter.


    :copyright: (c) 2016 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import logging
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqTimeout

logger = logging.getLogger('robo')


class SlackXmpp(ClientXMPP):
    def __init__(self, jid, password, username, rooms):
        """Construct a xmpp client.

        :param jid: Jid
        :param password: Slack password
        :param username: Bot name
        :param room: Chat rooms
        """
        ClientXMPP.__init__(self, jid, password)
        self.signal = None
        self.rooms = rooms
        self.nick = username
        self.add_event_handler('session_start', self.session_start)
        self.add_event_handler('groupchat_message', self.muc_message)

    def session_start(self, event):
        """Start session.

        :param event:
        """
        self.send_presence()
        logger.info('Finish to send presence')
        try:
            self.get_roster()
        except IqTimeout as e:
            logger.error(e)
        logger.info('Finish to get_roster()')
        rooms = self.rooms
        for room in rooms:
            self.plugin['xep_0045'].joinMUC(room.lstrip().rstrip(), self.nick,
                                            wait=False)
        logger.debug('Start session.')

    def muc_message(self, message):
        """Receive multi user chat message.

        :param msg:
        """
        if message['mucnick'] != self.nick and self.nick in message['body']:
            self.signal.send(message['body'], original=message, source='slack')


class Slack(object):
    def __init__(self, signal):
        """Construct a Slack adapter.

        :param signal: :class:`blinker.signal` Signal
        """
        logger.info('Start slack adapter.')
        password = os.environ['ROBO_SLACK_PASSWORD']
        room = os.environ['ROBO_SLACK_ROOM']
        team = os.environ['ROBO_SLACK_TEAM']
        username = os.environ['ROBO_SLACK_USERNAME']
        jid = '{0}@{1}.xmpp.slack.com'.format(username, team)
        logger.info('jid is `{0}`.'.format(jid))
        logger.info('room is `{0}`.'.format(room))

        #: Enable to join multi rooms.
        rooms = room.split(',')
        logger.info('Joining rooms are {0}.'.format(rooms))

        self.xmpp = SlackXmpp(jid, password, username, rooms)
        #: Add service discovery.
        self.xmpp.register_plugin('xep_0030')
        #: Add Multi-User chat.
        self.xmpp.register_plugin('xep_0045')
        #: Add XMPP ping.
        self.xmpp.register_plugin('xep_0199')
        self.xmpp.signal = signal
        logger.info('Finish to prepare connecting.')

    def say(self, message, **kwargs):
        """Send reply message to Slack.

        :param message: Message body
        :param **kwargs: kwargs['original'] is Sleekxmpp message
        """
        original = kwargs.get('original')
        self.xmpp.send_message(mto=original['from'].bare,
                               mbody=message, mtype='groupchat')

    def run(self):
        """ Run xmpp client. """
        if self.xmpp.connect():
            logging.info('Start xmpp client.')
            self.xmpp.process(block=True)
        else:
            logger.error('Cannot start xmpp client.')
