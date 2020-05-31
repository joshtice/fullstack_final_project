import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

from app import app

class AuthError(Exception):
    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message


def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise AuthError(
            error_code=401,
            error_message="Authorization header missing"
        )

    auth_header_elements = auth_header.split(' ')
    if auth_header_elements[0].lower() != 'bearer':
        raise AuthError(
            error_code=401,
            error_message="Authorization header must start with 'Bearer'"
        )
    elif len(auth_header_elements) == 1:
        raise AuthError(
            error_code=401,
            error_message="Token not found"
        )
    elif len(auth_header_elements) > 2:
        raise AuthError(
            error_code=401,
            error_message="Authorization header must be a bearer token",
        )
    else:
        return auth_header_elements[1]


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError(
            error_code=401,
            error_message="Permissions not included in JWT",
        )
    if permission not in payload['permissions']:
        raise AuthError(
            error_code=403,
            error_message="Correct permission not found - Access forbidden"
        )
    return True


def verify_decode_jwt(token):
    json_url = urlopen(f"https://{app.config['AUTH0_DOMAIN']}/.well-known/jwks.json")
    jwks = json.loads(json_url.read())
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError(
            error_code=401,
            error_message="Authorization malformed",
        )
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=app.config['ALGORITHMS'],
                audience=app.config['API_AUDIENCE'],
                issuer=f"https://{app.config['AUTH0_DOMAIN']}/"
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError(
                error_code=401,
                error_message="Token expired"
            )
        except jwt.JWTClaimsError:
            raise AuthError(
                error_code=401,
                error_message="Incorrect claims. Please check the audience and issuer"
            )
        except Exception:
            raise AuthError(
                error_code=401,
                error_message="Unable to parse authentication token"
            )
    else:
        raise AuthError(
            error_code=401,
            error_message="Unable to find the appropriate key"
        )


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)
        return wrapper
    return requires_auth_decorator
