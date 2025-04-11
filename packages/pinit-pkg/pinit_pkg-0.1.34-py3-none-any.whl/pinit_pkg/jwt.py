import jwt
from pinit_pkg.errors import UnauthorizedError

def parse_token(token: str):
    try:
        return jwt.decode(token, options={'verify_signature': False})
    except jwt.InvalidTokenError:
        raise UnauthorizedError('Invalid token format')

def get_headers(token: str):
    token = parse_token(token)
    return token.get('headers', {})

def get_payload(token: str):
    token = parse_token(token)
    return token.get('payload', {})
