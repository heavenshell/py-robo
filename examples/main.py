#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    main
    ~~~~

    Endpoint of robo.


    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
import logging
from functools import partial
from robo.robot import Robot


def main(args=None):
    """Main.

    :param args: :class:`argparse` Args
    """
    logging.basicConfig(level=args.verbose, format=Robot.debug_log_format)
    logger = logging.getLogger('robo')

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    get_path = partial(os.path.join, root)
    handler_path = get_path('robo/handlers')
    adapter_path = get_path('robo/adapters')
    logger.debug('Handler path is `{0}`'.format(handler_path))
    logger.debug('Adapter path is `{0}`'.format(adapter_path))

    robot = Robot(logger=logger)
    robot.setup_handlers(handler_path)
    robot.setup_adapters(adapter_path, args.adapter)
    robot.run(args.adapter)


def parse_options():
    """Parse options. """
    description = 'Dead simple bot framework'
    parser = argparse.ArgumentParser(description=description, add_help=False)
    parser.add_argument('-a', '--adapter', default='shell')
    parser.add_argument('-vv', '--verbose', default=logging.INFO, nargs='?',
                        const=logging.DEBUG)

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parse_options()
    main(args)
