# -*- coding: utf-8 -*-
"""
    robo.robot
    ~~~~~~~~~~

    Dead simple bot framework.

    robo is inspired by Ruboty.


    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import re
import inspect
import pkgutil
import logging
from blinker import signal
from robo.message import Message
from robo.utils import snakecase_to_pascalcase


class PluginLoader(object):
    """`PluginBase` is great library, but it has side effect.

    `PluginBase` delete `builtins`, for example, when using `print` function
    at plugin class, it raised error(TypeError: 'NoneType' object is not
    subscriptable).

    So we jsut create simple plugin loader.
    """
    def __init__(self, package):
        """Construct plugin loader.

        :param package: Package name
        """
        self.plugin_paths = []
        self.package = package

    def list_plugins(self, searchpath):
        """List plugin names.

        :param searchpath: Plugin paths
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
        return __import__(self.package + '.' + name,
                globals(), {}, ['__name__'])


class Robot(object):
    #: Default log format.
    debug_log_format = (
        '[%(asctime)s %(levelname)s][%(pathname)s:%(lineno)d]: %(message)s'
    )

    def __init__(self, name='robo', logger=None):
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
        self.logger.debug('Subscribing message is `{0}`.'.format(sender))
        handlers = self.handlers
        for handler in handlers:
            #: Message should start with robot's name(default is robo).
            trigger = self.trigger_pattern.match(sender)
            if trigger and 'regex' in handler:
                body = trigger.group(1)
                pattern = handler['regex']
                matched = pattern.match(body)
                if matched:
                    method = handler['method']
                    instance = handler['instance']
                    if hasattr(instance, method):
                        obj = getattr(instance, method)
                        if instance.__module__ == 'robo.handlers.help':
                            kwargs['docs'] = self.docs

                        send_to = '{0}.{1}'.format(instance.__module__, method)
                        message = Message(sender, match=matched,
                                          send_to=send_to, **kwargs)

                        result = obj(message)
                        #: Notify message to adapter.
                        self.notify_to_adapter(result, **kwargs)

    def notify_to_adapter(self, sender, **kwargs):
        """Notify message to adapter.

        :param sender: Message
        :param **kwargs: Data to be sent to receivers
        """
        #: Notify to all adapters.
        adapters = self.adapters
        for name in adapters:
            self.logger.debug('Notify `{0}` to `{1}.`'.format(sender, name))
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
                    self.logger.debug('Regex is `{0}.`'.format(regex))

                #: `description` is for help.
                #: `> robo help` will show all usages.
                description = plugin_kwargs['description'] if 'description' in \
                        plugin_kwargs else ''

                doc = 'description: {0}, pattern: {1}'.format(
                    description,
                    regex.pattern
                )
                self.docs.append(doc)
                method = {
                    'instance': instance,
                    'method': func_name,
                    'kwargs': plugin_kwargs,
                    'regex': regex,
                }
                methods.append(method)

        return methods

    def setup_adapters(self, path, adapter_name, package='robo.adapters'):
        """Setup adapters.

        :param path: Path to adapter
        :param adapter_name: Adapter name to run
        """
        #: Load adapter class which is specify boot arg.
        adapter_base = PluginLoader(package=package)
        plugin = adapter_base.load_plugin(adapter_name)
        adapter_class = getattr(plugin, snakecase_to_pascalcase(adapter_name))
        #: Register signal instance to adapter class.
        self.adapters[adapter_name] = adapter_class(self.handler_signal)
        self.logger.debug('Adapter `{0}` loaded.'.format(plugin))

    def run(self, adapter_name):
        """Run robot.

        :param adapter_name: Adapter name
        """
        self.logger.debug('Robo booting...')
        adapter = self.adapters[adapter_name]
        adapter.run()
