import jwt

def get_headers(token: str):
    return jwt.get_unverified_header(token)

def get_payload(token: str):
    return jwt.get_unverified_payload(token)
