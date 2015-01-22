robo
====
.. image:: https://travis-ci.org/heavenshell/py-robo.png?branch=master


Dead simple bot framework which is inspired by Ruby's `ruboty <https://github.com/r7kamura/ruboty>`_.


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

- `shell <https://github.com/heavenshell/py-robo/blob/master/robo/adapters/shell.py>`_
- `Slack <https://github.com/heavenshell/py-robo/blob/master/robo/adapters/slack.py>`_


Handler
-------
Handler provides various behaviors to your robot.

.. code:: python

  from robo.decorators import cmd

  class Ping(object):
      @cmd(regex=r'^ping', description='')
      def pong(self, message, **kwargs):
          return 'pong'

This handler matches message `ping` and return `pong` to chat service.


Bootstrap
---------
`example/main.py <https://github.com/heavenshell/py-robo/blob/master/examples/main.py>`_ is a example of bootstraping `robo`.

.. code:: python

  def main(args=None):
      #: `name` is bot's name.
      #: This arg is trigger of handler.
      robot = Robot(name=args.name, logger=logger)
      #: `register_default_handlers()` register default handlers.
      #: Default handlers are `help`, `ping`, `echo`.
      robot.register_default_handlers()
      #: Load given adapter name.
      robot.load_adapter(args.adapter)
      #: Run robot
      robot.run(args.adapter)
