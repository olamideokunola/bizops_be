from .JwtTokenManager import JwtTokenManager
from django.http import JsonResponse

class JwtMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        self.jwtManager = JwtTokenManager()

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        payload = self.jwtManager.decode_token(request)

        if payload != None:
            print('In JwtMiddleware, Payload is: ' + str(payload))
            request.user = payload['user'] if 'user' in payload else None
        else:
            request.user = None

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
