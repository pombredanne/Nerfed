import os

from nerfed import Application
from nerfed import Sub


class Settings(object):

    root = os.path.dirname(__file__)

    @property
    def templates_path(self):
        return os.path.join(self.root, 'templates')


class Hello(Sub):

    def __init__(self, app, path, instance_name=None):
        super(Hello, self).__init__(app, path)

    def get(self, request):
        return self.app.render(request, 'index.html')


class Demo(Application):

    def __init__(self):
        super(Demo, self).__init__(Settings())
        self.register('localhost', Hello, '^/$')

demo = Demo()
