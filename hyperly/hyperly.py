import os

from nerfed import Sub
from nerfed import Imperator
from nerfed import Application
from nerfed.db import MongoDB
from nerfed.properties import URL as URLProperty
from nerfed.properties import String
from nerfed.properties import Integer
from nerfed.shared import random_string


class Settings(object):

    root = os.path.dirname(__file__)

    URL = 'http://127.0.0.1:8000'
    TEMPLATES_PATH = os.path.join(root, 'templates')
    MONGODB_SERVER = 'localhost:27017'
    MONGODB_DATABASE_NAME = 'hyperly'
    STATIC_URL = 'http://localhost:8001/static/'
    COOKIE_DOMAIN = '127.0.0.1'


class URL(Imperator):

    id = Integer(null=True, primary_key=True, autoincrement=True)
    url = URLProperty()
    short_url = String(null=True)

    def create_short_url(app, imperator, ok):
        if not ok:
            return
        imperator.short_url = random_string(5)
        app.db.urls.insert(imperator.dict())
        return True

    actions = (create_short_url,)


class URLRedirect(Sub):

    def get(self, request):
        short_url = request.path_match['short_url']
        url = self.app.db.urls.find_one(dict(short_url=short_url))
        url = url['url']
        return self.app.redirect(url)


class URLInfo(Sub):

    def get(self, request):
        short_url = request.path_match['short_url']
        url = self.app.db.urls.find_one(dict(short_url=short_url))
        return self.app.render(request, 'info.html', url=url)


class Index(Sub):

    def get(self, request):
        return self.app.render(request, 'index.html', form=URL())

    def post(self, request):
        short_urlize = URL(request.POST)
        if short_urlize(self.app):
            return self.app.redirect('/%s+' % short_urlize.short_url)
        return self.app.render(request, 'index.html', form=short_urlize)


class Hyperly(Application):

    def __init__(self):
        super(Hyperly, self).__init__(Settings())
        self.db = MongoDB(self.settings)
        self.index = self.register(Index, r'^/$')
        self.url_redirect = self.register(URLRedirect, r'^/(?P<short_url>\w+)$')
        self.index = self.register(Index, r'^/$')
        self.url_info = self.register(URLInfo, r'^/(?P<short_url>\w+)\+$')

hyperly = Hyperly()
