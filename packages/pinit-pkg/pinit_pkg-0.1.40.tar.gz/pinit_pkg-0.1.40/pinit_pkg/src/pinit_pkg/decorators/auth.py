import jwt
import pydantic

from functools import wraps
from typing import Any, Callable, Dict
from loguru import logger

from pinit_pkg.errors import UnauthorizedError
from pinit_pkg.schemas import AuthHeaders
from pinit_pkg.kms import kms_verify_signature


def auth(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(event: Dict, context: Any) -> Any:
        headers = event.get('headers', {})

        try:
            auth_header = AuthHeaders(**headers)
            token = auth_header.authorization.split(' ')[1]

            jwt_headers = jwt.get_unverified_header(token)
            if not jwt_headers.get('kid'):
                raise UnauthorizedError('Invalid token: missing key ID')

            if not kms_verify_signature(token, jwt_headers.get('kid')):
                raise UnauthorizedError('Invalid token signature')

            return func(event, context)

        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid JWT token: {str(e)}")
            raise UnauthorizedError('Invalid token format')
        except pydantic.ValidationError as e:
            logger.error(f"Auth error: {str(e)}")
            raise UnauthorizedError("Unauthorized")

    return wrapper
