0.5.6
-----
* Exclude `examples` directory.

0.5.5
-----
* Add Python3.5 to ``tox.ini`` and ``.travis.yml``.
* Add ``None`` check for avoid ``AttributeError: 'NoneType'`` if handler publish ``None``.

0.5.4
-----
* Fix typo at ``adapters.slack.py``.
* Add ``sleekxmpp.exceptions.IqTimeout`` to ``adapters.slack.py`` for avoid request timeout.

0.5.3
-----
* Change ``logger.debug to logger.info`` Slack logger.

0.5.2
-----
* Add ``**kwargs`` to handler method.

0.5.1
-----
* Delete logger arg from ``adapters.shell``.
* Fix test docstring.
* Add ``options`` to ``robot`` constructor.

0.5.0
-----
* Inject robot name to handler class, if handler class has ``robot_name`` property.

0.4.9
-----
* Inject signal object to handler class, if handler class has ``signal`` property.
* Add ``__repr__`` to ``robo.message.Message``.

0.4.8
-----
* Add `shutdown` method to ``robo.robot``.

0.4.7
-----
* Refactor method name `setup_adapters()` to `load_adapter()`.

0.4.6
-----
* Add _compat for Python2 and Python3 compatible.
* Add Unicode test.
* Fix pep8 violation.
* Fix to log regex pattern more detail.

0.4.5
-----
* Add ``robo.robot.register_default_handlers()`` for register default handlers.

0.4.4
-----
* Delete ununsed param ``path`` from ``robo.robot.setup_adapters``.

0.4.3
-----
* Improve joining multi chat room.

0.4.2
-----
* Improve format display ``help`` result.

0.4.1
-----
* Tiny refactoring.

0.4.0
-----
* Add missing option. ``missing=True`` is called only when any handler doesn't match given message.

0.3.1
-----
* Improve format display ``help`` result.

0.3
---
* Add chat room option.

0.2
---
* Add Slack adapter.

0.1
---
* First release.
