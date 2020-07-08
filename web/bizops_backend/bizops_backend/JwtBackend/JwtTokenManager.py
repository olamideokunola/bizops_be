import jwt
import json

class JwtTokenManager:
    token = None

    def __get_credentials_from_request(self, request):
        # Get param from request body as python object
        print(request.GET)
        # print(json.loads(request.body))     
        params = request.GET
        # params = json.loads(request.body)
        
        # Get individual params
        username = params['username'] if 'username' in params.keys() else None
        password = params['password'] if 'password' in params.keys()  else None

        return {'username': username, 'password': password}

    def create_token(self, payload):
        """Create token"""
       # credentials = self.__get_credentials_from_request(request)
        # print('payload:--- ' + payload['username'])

        key='secret'
        # undd = payload['username']
        self.token = jwt.encode(payload, key, algorithm='HS256')
        print('token: ' + str(self.token))

        return self.token

    def get_token(self, request):
        """Gets token from request or return None"""
        if self.get_authorization_header(request) != None:
            auth = self.get_authorization_header(request).split()

            # print('In Token Manager, token auth: ' + str(auth))

            if not auth or auth[0].lower() != 'bearer':
                print('auth: '+ 'No auth')
                return None

            return auth[1]
        else:
            print('No Authorization header!')
            return None

    def decode_token(self, request):

        print('In decode token')
        token = self.get_token(request)
        try:
            return jwt.decode(token, 'secret', algorithm='HS256')
        except jwt.exceptions.InvalidTokenError:
            msg = "decode failure, Invalid token!"
            return None


    def authenticate(self, request):
        """
        Simple token based authentication.
        Clients should authenticate by passing the token key in the "Authorization"
        HTTP header, prepended with the string "Token ".  For example:
        Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
        """

        if self.get_authorization_header(request) != None:
            auth = self.get_authorization_header(request).split()

            print('auth: ' + str(auth))

            if not auth or auth[0].lower() != 'bearer':
                print('auth: '+ 'No auth')
                return None
            #try:
            token = auth[1]#.decode()
            # except UnicodeError:
            #     msg = _('Invalid token header. Token string should not contain invalid  characters.')
            #     raise exceptions.AuthenticationFailed(msg)

            return self.authenticate_credentials(token)

    def authenticate_credentials(self, payload):

        decoded_dict = jwt.decode(payload, 'secret', algorithm='HS256')

        username = decoded_dict.get('username', None)

        # try:
        #     usr = User.objects.get(username=username)
        # except model.DoesNotExist:
        #     raise exceptions.AuthenticationFailed(_('Invalid token.'))

        # if not usr.is_active:
        #     raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        # if expiry < datetime.date.today():
        #     raise exceptions.AuthenticationFailed(_('Token Expired.'))

        return username

    def get_authorization_header(self, request):
        return request.headers['Authorization'] if 'Authorization' in request.headers else None