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
