# -*- coding: utf-8 -*-
"""
    robo.utils
    ~~~~~~~~~~

    Just utilities.


    :copyright: (c) 2014 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""


def snakecase_to_pascalcase(value):
    """Convert snakecase to pascalcase.

    >>> snakecase_to_pascalcase('foo_bar')
    'FooBar'
    >>> snakecase_to_pascalcase('foo__bar')
    'FooBar'
    >>> snakecase_to_pascalcase('foo')
    'Foo'

    :param value:
    """
    items = value.split('_')

    return items[0].capitalize() + ''.join(x.title() for x in items[1:])
