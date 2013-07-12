import os

from nerfed import Sub
from nerfed import Imperator
from nerfed import Application
from nerfed.db import SQLAlchemyDB
from nerfed.properties import String
from nerfed.properties import Integer


class Message(Imperator):
    id = Integer(primary_key=True, autoincrement=True, nullable=True)
    message = String()


class Settings(object):

    root = os.path.dirname(__file__)

    TEMPLATES_PATH = os.path.join(root, 'templates')
    SQLALCHEMY = dict(url="sqlite:///db.sqlite")


class Hello(Sub):

    def __init__(self, app, parent, path, instance_name=None):
        super(Hello, self).__init__(app, parent, path)
        self.app.db.register(Message)

    def get(self, request):
        return self.app.render(request, 'index.html')


class Demo(Application):

    def __init__(self):
        super(Demo, self).__init__(Settings())
        self.db = SQLAlchemyDB(self.settings.SQLALCHEMY)
        self.register(Hello, '^/$')

demo = Demo()
