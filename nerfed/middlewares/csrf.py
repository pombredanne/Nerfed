from ..shared import random_string


class CSRF(object):

    COOKIE_NAME = 'csrf_token'

    def _cookie_csrf_token(self, request):
        try:
            return request.cookies[CSRF.COOKIE_NAME]
        except KeyError:
            token = random_string(128)
            request.cookies[CSRF.COOKIE_NAME] = token
            return token

    def process_request_before_view(self, app, request):
        cookie_csrf_token = self._cookie_csrf_token(request)

        if request.method == 'POST':
            request_csrf_token = request.POST.get(CSRF.COOKIE_NAME, None)
            if cookie_csrf_token != request_csrf_token:
                return app.forbidden(request)

    def process_response_before_answer(self, app, request, response):
        # XXX: 36000 is suspicious I can't find the right value
        # maybe use expires ?
        response.set_cookie(CSRF.COOKIE_NAME, self._cookie_csrf_token(request), max_age=36000, domain=app.settings.COOKIE_DOMAIN)        
