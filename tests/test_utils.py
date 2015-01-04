# -*- coding: utf-8 -*-
"""
    Add comment here
    ~~~~~~~~~~~~~~~~

    Add descripton here


    :copyright: (c) 2014 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from unittest import TestCase
from robo.utils import snakecase_to_pascalcase


class TestUtils(TestCase):
    def test_should_convert_to_pascalcase(self):
        """ snakecase_to_pascalcase(foo_bar) should convert to FooBar. """
        ret = snakecase_to_pascalcase('foo_bar')
        self.assertEqual(ret, 'FooBar')

    def test_should_convert_to_pascalcase2(self):
        """ snakecase_to_pascalcase(foo) should convert to Foo. """
        ret = snakecase_to_pascalcase('foo')
        self.assertEqual(ret, 'Foo')

    def test_should_convert_to_pascalcase3(self):
        """ snakecase_to_pascalcase(foo__bar) should convert to FooBar. """
        ret = snakecase_to_pascalcase('foo__bar')
        self.assertEqual(ret, 'FooBar')
