import re


REGROUP = re.compile(r'\(\?P<\w+>[^\)]+\)')
REGROUPNAME = re.compile('<(\w+)>')


def clean_regex_path(path):
    if path.startswith('^'):
        path = path[1:]
    if path.endswith('$'):
        path = path[:-1]
    return path


class Sub(object):

    def __init__(self, app, parent, path):
        self.app = app
        self.subs = list()
        self.parent = parent
        self.path = re.compile(path)
        path = clean_regex_path(path)
        path = self.parent.full_path(self) + path
        path = clean_regex_path(path)
        self._full_path = path
        
        groups = REGROUP.findall(self._full_path)
        format = path
        for group in groups:
            name = REGROUPNAME.findall(group)[0]
            format = format.replace(group, '%%(%s)s' % name)
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
            return self.app.forbidden()
        if hasattr(self, method.lower()):
            return getattr(self, method.lower())(request)
        return self.app.forbidden(request)

    def reverse(self, **kwargs):
        print self.format, kwargs
        return self.format % kwargs
