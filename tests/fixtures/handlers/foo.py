# -*- coding: utf-8 -*-
from robo.decorators import cmd

class Foo(object):
    @cmd(regex=r'^hi', description='test hi')
    def hi(self, message, **kwargs):
        return 'hi'

    @cmd(regex=r'^hello')
    def hello(self, message, **kwargs):
        return 'hello'
