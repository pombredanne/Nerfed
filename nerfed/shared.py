import random
import string

from webob import Response


class ErrorResponses(object):

    def not_found(self, request):
        return Response('<h1>Not found</h1>', 404)

    def internal_server_error(self, request):
        return Response('<h1>Internal Server Error</h1>', 500)

    def forbidden(self, request):
        return Response('<h1>Forbidden</h1>', 403)


def random_string(N):
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(N))
