from django.db import close_old_connections
from jwt import decode as jwt_decode
from django.conf import settings
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from users.models import User
 
class TokenAuthMiddleware:
    """
    Custom token auth middleware
    """
 
    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner
 
    def _authenticate_credentials(self, token):
        user = None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = 'Invalid authentication. Could not decode token.'
            return None, msg

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            return None, msg

        if not str(user.jwt_secret)==payload['secret']:
            msg = 'Token is not valid.'
            return None, msg

        if not user.is_active:
            msg = 'This user has been deactivated.'
            return None, msg

        return user, None

    def __call__(self, scope):
 
        # Close old database connections to prevent usage of timed out connections
        close_old_connections()
 
        user = None
        error = None
        # Get the token
        token = parse_qs(scope["query_string"].decode("utf8")).get("token",None)
        if token:
            user, error = self._authenticate_credentials(token[0])
        return self.inner(dict(scope, user=user,error=error))