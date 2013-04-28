import re
from logging import getLogger
from traceback import print_exc

from webob import Request
from webob import Response
from jinja2 import Environment
from jinja2 import FileSystemLoader

from shared import ErrorResponses


log = getLogger(__file__)


class Application(ErrorResponses):

    def __init__(self, settings=None):
        self.settings = settings
        self.subs = list()
        self.app = self

        self.loader = FileSystemLoader(settings.templates_path)

    def register(self, domain, sub_class, path, instance_name=None):
        log.debug('registred %s' % sub_class)
        sub = sub_class(self, re.compile(path), instance_name)
        self.subs.append((re.compile(domain), sub))

    def _match_path(self, match, path, subs):
        match = None
        for sub in subs:
            submatch = sub.path.match(path)
            if submatch:
                # it is the good path
                matched = submatch.groupdict()
                if matched:
                    matched.update(match)
                else:
                    matched = match
                subpath = path[submatch.end():]
                if subpath:
                    # try subs from this sub
                    o = self._match_path(submatch, subpath, sub.subs)
                    if o[0]:
                        # a sub of this sub is a match return it
                        return o
                else:
                    # if it matched but is not a subsub then it's the one
                    # that match (and to repeat it: it's not a sub of sub!)
                    return submatch, sub
            # else continue
        # None matched
        return None, None

    def __call__(self, environ, start_response):
        request = Request(environ)
        for domain, sub in self.subs:
            log.debug('try to match %s @ %s' % (sub, domain))
            # first match the domain if any
            domain_match = domain.match(request.server_name)
            if not domain_match:
                continue
            # try to match the path
            path = request.path
            path_match, sub = self._match_path(dict(), path, [sub])
            if not path_match:
                continue
            # found the good sub, just call __call__ :)
            request.path_match = path_match
            request.domain_match = domain_match
            try:
                response = sub(request)
            except Exception, e:
                print_exc()
                response = self.internal_server_error(request)
                return response(environ, start_response)
            return response(environ, start_response)
        response = self.not_found(request)
        return response(environ, start_response)

    def render(self, request, path, **kwargs):
        response = Response(status=200)
        template = self.loader.load(Environment(), path)
        kwargs['settings'] = self.settings
        kwargs['request'] = request
        response.text = template.render(**kwargs)
        return response
