import jwt
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User

def authenticate_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
    except:
        msg = 'Invalid authentication. Could not decode token.'
        raise exceptions.AuthenticationFailed(msg)

    try:
        user = User.objects.get(pk=payload['id'])
    except User.DoesNotExist:
        msg = 'No user matching this token was found.'
        raise exceptions.AuthenticationFailed(msg)

    if (user.last_activity is None) or (user.last_activity + timedelta(hours=24)) < timezone.now():
        msg = 'Token expired'
        raise exceptions.AuthenticationFailed(msg)

    if not str(user.jwt_secret)==payload['secret']:
        msg = 'Token is not valid.'
        raise exceptions.AuthenticationFailed(msg)

    if not user.is_active:
        msg = 'This user has been deactivated.'
        raise exceptions.AuthenticationFailed(msg)

    User.objects.filter(pk=payload['id']).update(last_activity = timezone.now())

    return (user, token)
class HeaderAuthenticator(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None
        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None

        return authenticate_jwt_token(token)

class CookieAuthenticator(authentication.BaseAuthentication):
    def authenticate(self, request):
        request.user = None

        auth_token = request.COOKIES.get('token')

        if not auth_token:
            return None

        return authenticate_jwt_token(auth_token)

class QueryParamsAuthenticator(authentication.BaseAuthentication):
    def authenticate(self, request):
        request.user = None

        auth_token = request.GET.get('token')

        if not auth_token:
            return None

        return authenticate_jwt_token(auth_token)
