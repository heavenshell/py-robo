robo
====
.. image:: https://travis-ci.org/heavenshell/py-robo.png?branch=master


Dead simple bot framework which is inspired by Ruby's `ruboty <https://github.com/r7kamura/ruboty>_`.


Why reinvent the wheel
----------------------

I Love Python and I'm not good at Node.js(hubot), Ruby(Ruboty).

`Err <https://github.com/gbin/err>`_ is pluggable but it's too complex for me.

`brutal <http://brutal.readthedocs.org/en/latest/index.html>`_ is also pluggable but I don't wont to write config file.

So I reinvent the wheel.

Architecture
------------

Message flow.

.. code:: text


                              +--[handler a]--+
                              |               |
  [chat service]-->[adapter]--+--[handler b]--+--[adapter]-->[chat service]
                              |               |
                              +--[handler c]--+


Adapter
-------

Adapter is interface of chat services receive message and send message to chat service.

Robo includes two adapters.

- shell
- Slack


Handler
-------
Handler provides various behaviors to your robot.

.. code:: python

  from robo.decorators import cmd

  class Ping(object):
      @cmd(regex=r'^ping', description='')
      def pong(self, message):
          return 'pong'

This handler matches message `ping` and return `pong` to chat service.


How to create plugins
---------------------
TBD
