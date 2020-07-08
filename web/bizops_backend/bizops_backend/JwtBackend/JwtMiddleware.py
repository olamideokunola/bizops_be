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
            # print('In JwtMiddleware, Payload is: ', payload)
            if 'user' in payload:
                print('user in payload')
                request.user = payload['user']
                # request.username = payload['user']['username'] 
            elif 'username' in payload:
                print('In JWT middleware username in payload')
                request.user = payload
                # request.username = payload['username'] 
                print('request.user is: ', request.user)
            else:
                print('In JwtMiddleware, user or username not in payload!')
                request.user = None
        else:
            print('In JwtMiddleware, no Payload!')
            request.user = None

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
