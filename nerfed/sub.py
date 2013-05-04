import re


REGROUP = re.compile(r'\(\?P<\w+>[^\)]+\)')
REGROUPNAME = re.compile('<(\w+)>')


class Sub(object):

    def __init__(self, app, parent, path):
        self.app = app
        self.subs = list()
        self.path = re.compile(path)

        self._full_path = self.parent.full_path(self) + path

        groups = REGROUP.findall(self._full_path)
        format = path
        for group in groups:
            name = REGROUPNAME.findall(group)[0]
            format.replace(group, '%%(%s)' % name)
        self.format = format

    def full_path(self, sub):
        return self._full_path

    def register(self, sub_class, path):
        sub = sub_class(self.app, self, path)
        self.subs.append(sub)
        return sub

    def __repr__(self):
        return '<%s @ %s>' % (type(self).__name__, self.path.pattern)

    def __call__(self, request):
        method = request.method
        if method not in ('GET', 'HEAD', 'POST', 'PUT'):
            return self.forbidden()
        if hasattr(self, method.lower()):
            return self.get(request)
        return self.forbidden()

    def reverse(self, **kwargs):
        return self.format % kwargs

        
