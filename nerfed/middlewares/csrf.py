from ..shared import random_string


class CSRF(object):

    def _cookie_csrf_token(self, request):
        try:
            return request.cookies[CSRF.COOKIE_NAME]
        except:
            return random_string(512)

    def process_request_before_view(self, app, request):
        cookie_csrf_token = self._cookie_csrf_token(request)

        if request.method == 'POST':
            request_csrf_token = request.POST.get('csrfmiddlewaretoken', None)

            if cookie_csrf_token != request.csrf_token:
                return app.forbidden(request)

    def process_response_before_answer(self, app, request, response):
        response.set_cookie(CSRF.COOKIE_NAME, self._cookie_csrf_token(request))
        
