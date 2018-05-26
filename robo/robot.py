# -*- coding: utf-8 -*-
"""
    robo.robot
    ~~~~~~~~~~

    Dead simple bot framework.

    robo is inspired by Ruboty.


    :copyright: (c) 2018 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import re
import inspect
import pkgutil
import logging
from blinker import signal
from robo.message import Message
from robo.utils import snakecase_to_pascalcase
from robo._compat import to_unicode


class PluginLoader(object):
    """`PluginBase` is great library, but it has side effect.

    `PluginBase` delete `builtins`, for example, when using `print` function
    at plugin class, it raised error(TypeError: 'NoneType' object is not
    subscriptable).

    So just create a simple plugin loader.
    """
    def __init__(self, package):
        """Construct plugin loader.

        :param package: Package name
        """
        self.plugin_paths = []
        #: Base plugin package name.
        self.package = package

    def list_plugins(self, searchpath):
        """List plugin names.

        :param searchpath: List of plugin paths
        """
        rv = []
        for _, modname, ispkg in pkgutil.iter_modules(searchpath):
            if ispkg is False:
                #: Register only files.
                #: Package(directoires) are ignored.
                rv.append(modname)

        return sorted(rv)

    def load_plugin(self, name):
        """Load plugin.

        :param name: Plugin file name
        """
        package = self.package + '.' + name
        return __import__(package, globals(), {}, ['__name__'])


class Robot(object):
    #: Default log format.
    debug_log_format = (
        '[%(asctime)s %(levelname)s][%(pathname)s:%(lineno)d]: %(message)s'
    )

    def __init__(self, name='robo', logger=None, **kwargs):
        """Construct a robot.

        :param name: Robot name
        :param logger: :class:`logging` Logger
        """
        self.name = name
        #: Trigger robot's name.
        #: ex.
        #:   > robo ping
        #:   pong
        self.trigger_pattern = re.compile(r'\A@?{0}:?\s+(.*)'.format(name))
        self.adapters = {}
        self.handlers = []
        self.docs = []
        self.options = kwargs

        if logger is None:
            logging.basicConfig(level=logging.INFO,
                                format=self.debug_log_format)
            logger = logging.getLogger('robo')
        self.logger = logger

        #: Create signals for receive events.
        self.handler_signal = signal('robo.handler')
        #: Register subscriber.
        self.handler_signal.connect(self.handler_subscriber, weak=True)

    def handler_subscriber(self, sender, **kwargs):
        """Subscriber.

        Receive message from adapter.

        If message is matched, send message object to handlers
        and notify to adapter.

        :param sender: Received message
        :param **kwargs: Data to be sent to receivers
        """
        if sender is None:
            self.logger.info('Subscribing message is None.')
            return

        message = to_unicode(sender)
        message_format = 'Subscribing message is `{0}`'
        self.logger.debug(message_format.format(message.encode('utf-8')))

        #: Message should start with robot's name(default is robo).
        trigger = self.trigger_pattern.match(message)
        if trigger is None:
            return

        #: Delete robot's name.
        #: > robo ping
        #: body would be `ping`.
        body = trigger.group(1)

        #: `missing` is called only when any handler doesn't match
        #: given message.
        missings = []
        matched_count = 0
        unmatched_count = 0

        handlers = self.handlers
        for handler in handlers:
            if 'regex' in handler:
                if handler['missing'] is True:
                    missings.append(handler)
                    continue

                pattern = handler['regex']
                matched = pattern.match(body)
                if matched:
                    ret = self.trigger_handler(message, handler, matched,
                                               **kwargs)
                    if ret is True:
                        matched_count += 1
                else:
                    unmatched_count += 1

        if matched_count == 0 and unmatched_count > 0:
            for missing_handler in missings:
                if 'regex' in missing_handler:
                    pattern = missing_handler['regex']
                    matched = pattern.match(body)
                    if matched:
                        self.trigger_handler(message, missing_handler,
                                             matched, **kwargs)

    def trigger_handler(self, sender, handler, matched, **kwargs):
        """Execute handler class if trigger condition all matched.

        If handler was decorated like `room='^random@.*'`,
        then check incoming message contains chat room and matched.

        >>> class(object):
        >>>    @cmd(regex='^hello$', room='^random@.')
        >>>    def hello(message **kwargs):
        >>>        return 'hello random'
        >>>
        >>>    @cmd(regex='^hello$')
        >>>    def hello2(message **kwargs):
        >>>        return 'hello'

        If incoming message is from room `@random`,
        method `hello()` and `hello2()` are matched.
        If incoming message is from room `@general`,
        only `hello2()` is matched.

        :param sender: Incoming message
        :param handler: Handler class instance
        :param matched: :class: `re.match` Matched object
        :param **kwargs: Data to be sent to receivers
        """
        if handler.get('room', None) is not None:
            #: Exit if handler method decorated with `room`,
            #: but incoming message not contained `room` or `room` is not
            #: matched.
            if kwargs.get('room', None) is None:
                return False

            if not handler['room'].match(kwargs.get('room')):
                return False

        method = handler['method']
        instance = handler['instance']
        if hasattr(instance, method):
            obj = getattr(instance, method)
            if instance.__module__ == 'robo.handlers.help':
                kwargs['docs'] = self.docs

            send_to = '{0}.{1}'.format(instance.__module__, method)
            message = Message(sender, match=matched,
                              send_to=send_to, **kwargs)

            result = obj(message, **kwargs)
            #: Notify message to adapter.
            self.notify_to_adapter(result, **kwargs)

            return True

        return False

    def notify_to_adapter(self, sender, **kwargs):
        """Notify message to adapter.

        :param sender: Message
        :param **kwargs: Data to be sent to receivers
        """
        #: Notify to all adapters.
        if sender is None:
            return
        adapters = self.adapters
        message_format = 'Notify `{0}` to `{1}.`'
        for name in adapters:
            self.logger.debug(message_format.format(sender.encode('utf-8'),
                              name))
            adapters[name].say(sender, **kwargs)

    def setup_handlers(self, paths, package='robo.handlers'):
        """Setup handlers.

        :param paths: Handler paths
        :param package: Package name
        """
        if not isinstance(paths, list):
            paths = [paths]

        handler_base = PluginLoader(package=package)
        handler_names = handler_base.list_plugins(searchpath=paths)
        for name in handler_names:
            plugin = handler_base.load_plugin(name)
            handler_class = getattr(plugin, snakecase_to_pascalcase(name))
            handler_obj = handler_class()
            if hasattr(handler_obj, 'signal'):
                handler_obj.signal = self.handler_signal
                message = 'Injected signal to handler `{0}`.'
                self.logger.debug(message.format(handler_class))

            if hasattr(handler_obj, 'robot_name'):
                handler_obj.robot_name = self.name
                message = 'Injected robot name to `{0}`.'
                self.logger.debug(message.format(handler_class))

            if hasattr(handler_obj, 'options'):
                handler_obj.options = self.options
                message = 'Injected options to `{0}`.'
                self.logger.debug(message.format(handler_class))

            #: List all handlers method.
            methods = self.parse_handler_methods(handler_obj)
            self.handlers.extend(methods)
            self.logger.debug('Handler `{0}` loaded.'.format(plugin))

    def parse_handler_methods(self, instance):
        """Parse plugin methods.

        List all handlers method.

        :param instance: Handler instance object
        """
        methods = []
        for func_name, func in inspect.getmembers(instance, inspect.ismethod):
            #: Handler's method was decorated with @cmd(),
            if getattr(func, '__robo_event', False):
                plugin_kwargs = getattr(func, '__robo_kwargs', {})
                regex = None
                #: Default regex flag is ignorecase.
                regex_flags = re.IGNORECASE
                if 'flags' in plugin_kwargs:
                    #: Regex flags.
                    regex_flags = plugin_kwargs['flags']
                    self.logger.debug('Regex flag is `{0}`'.format(regex_flags))

                if 'regex' in plugin_kwargs:
                    regex = re.compile(plugin_kwargs['regex'], regex_flags)
                    self.logger.debug('Regex is `{0}.`'.format(regex.pattern))

                missing = False
                if 'missing' in plugin_kwargs:
                    missing = True
                    self.logger.debug('Missing is `{0}`'.format(missing))

                room = None
                if 'room' in plugin_kwargs:
                    room = re.compile(plugin_kwargs['room'], re.IGNORECASE)
                    self.logger.debug('Room regex is `{0}`.'.format(room))

                #: `description` is for help.
                #: `> robo help` will show all usages.
                description = plugin_kwargs['description'] if 'description' in \
                    plugin_kwargs else ''

                doc = {
                    'robot_name': self.name,
                    'description': description,
                    'pattern': regex.pattern
                }
                self.docs.append(doc)
                method = {
                    'instance': instance,
                    'method': func_name,
                    'kwargs': plugin_kwargs,
                    'regex': regex,
                    'room': room,
                    'missing': missing
                }
                methods.append(method)

        return methods

    def load_adapter(self, adapter_name, package='robo.adapters'):
        """Setup adapters.

        :param adapter_name: Adapter name to run
        """
        #: Load adapter class which is specify boot arg.
        adapter_base = PluginLoader(package=package)
        plugin = adapter_base.load_plugin(adapter_name)
        adapter_class = getattr(plugin, snakecase_to_pascalcase(adapter_name))
        #: Register signal instance to adapter class.
        self.adapters[adapter_name] = adapter_class(self.handler_signal)
        self.logger.debug('Adapter `{0}` loaded.'.format(plugin))

    def register_default_handlers(self):
        """Register default handlers.

        Default handlers are `robo.handlers.echo`, `robo.handlers.help`,
        `robo.handlers.ping`.
        """
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'handlers')
        self.setup_handlers([path])

    def shutdown(self):
        """Shutdown.

        If handler has shutdown method, call it.
        """
        handlers = self.handlers
        for handler in handlers:
            if hasattr(handler['instance'], 'shutdown'):
                handler['instance'].shutdown()

    def run(self, adapter_name):
        """Run robot.

        :param adapter_name: Adapter name
        """
        self.logger.debug('Robo booting...')
        adapter = self.adapters[adapter_name]
        adapter.run()
