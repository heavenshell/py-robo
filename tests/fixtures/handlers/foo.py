# -*- coding: utf-8 -*-
from robo.decorators import cmd


class Foo(object):
    signal = None

    response = None

    options = None

    @cmd(regex=r'^hi', description='test hi')
    def hi(self, message, **kwargs):
        return 'hi'

    @cmd(regex=r'^hello')
    def hello(self, message, **kwargs):
        return 'hello'

    @cmd(regex=r'^goodbye', room=r'^@random')
    def goodbye(self, message, **kwargs):
        return 'goodbye @random'

    @cmd(regex=r'^goodbye', room=r'^@general')
    def goodbye2(self, message, **kwargs):
        return 'goodbye @general'

    @cmd(regex=r'^goodbye')
    def goodbye3(self, message, **kwargs):
        return 'goodbye all'

    @cmd(regex=r'.+', room=r'^missing', missing=True)
    def missing(self, message, **kwargs):
        return 'missing1'

    @cmd(regex=r'^foo$', room=r'^missing')
    def missing2(self, message, **kwargs):
        return 'missing2'

    def shutdown(self):
        self.response = 'shutdown'
