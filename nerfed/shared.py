from webob import Response


class ErrorResponses(object):

    def not_found(self, request):
        return Response('<h1>Not found</h1>', 404)

    def internal_server_error(self, request):
        return Response('<h1>Internal Server Error</h1>', 500)

    def forbidden(self, request):
        return Response('<h1>Forbidden</h1>', 403)
