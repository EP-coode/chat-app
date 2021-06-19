import os

from flask import request
from functools import wraps
import jwt

token_secret = os.getenv(
    "TOKEN_SECRET", "yoursuperstrongpassword123")


def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(' ')[1]
        except:
            return 'missing auth token', 403

        try:
            token_payload = jwt.decode(
                auth_token, token_secret, algorithms=["HS256"])
        except:
            return 'invalid auth token', 403

        return f(token_payload=token_payload)

    return decorated
