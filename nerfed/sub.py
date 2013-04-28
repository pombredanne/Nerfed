import re

from shared import ErrorResponses


class Sub(ErrorResponses):

    application_name = None
    name = None

    def __init__(self, app, path, instance_name=None):
        self.app = app
        self.path = path
        self.subs = list()
        self.instance_name = instance_name

    def register(self, sub_class, path, instance_name=None):
        self.subs.append(sub_class(self.app, re.compile(path)))

    def __repr__(self):
        return '<%s @ %s>' % (type(self).__name__, self.path.pattern)

    def __call__(self, request):
        method = request.method
        if method == 'GET' and hasattr(self, 'get'):
            return self.get(request)
        return self.not_found()
