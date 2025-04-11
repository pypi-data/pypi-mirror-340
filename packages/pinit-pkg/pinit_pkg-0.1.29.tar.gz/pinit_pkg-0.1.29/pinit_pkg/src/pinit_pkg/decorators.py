import time
import jwt
import pydantic

from functools import wraps
from typing import Any, Callable, Dict
from loguru import logger

from .errors import UnsupportedMediaTypeError, BadRequestError, NotFoundError, UnauthorizedError
from .request import parse_headers
from .responses import handle_response, response_error
from .schemas import AuthHeaders


def execution_time(func: Callable) -> Callable:
    """Decorator that prints the execution time of a function.

    Args:
        func (Callable): Function to be decorated

    Returns:
        Callable: Wrapped function
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"Function {func.__name__} took {end_time - start_time:.4f} seconds to execute")
        return result
    return wrapper


def lambda_handler(func: Callable) -> Callable:
    """Decorator that logs Lambda handler's event, context and response, checks headers and formats the response.

    Args:
        func (Callable): Lambda handler function to be decorated

    Returns:
        Callable: Wrapped function that handles logging and response formatting
    """
    @wraps(func)
    def wrapper(event: Dict, context: Any) -> Any:
        logger.info(f"Lambda event: {event}")
        logger.info(f"Lambda context: {context}")

        try:
            parse_headers(event)
            response = func(event, context)
            return handle_response(response)
        except NotFoundError as e:
            logger.error(f"Not found: {str(e)}")
            return handle_response(response_error(404, str(e)))
        except UnsupportedMediaTypeError as e:
            logger.error(f"Unsupported media type: {str(e)}")
            return handle_response(response_error(415, str(e)))
        except BadRequestError as e:
            logger.error(f"Bad request: {str(e)}")
            return handle_response(response_error(400, e.message(), e.errors()))
        except UnauthorizedError as e:
            logger.error(f"Unauthorized: {str(e)}")
            return handle_response(response_error(401, str(e)))
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return handle_response(response_error(500, str(e)))
    return wrapper


def auth(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(event: Dict, context: Any) -> Any:
        headers = event.get('headers', {})

        try:
            # Validate Authorization header format
            auth_header = AuthHeaders(**headers)
            token = auth_header.authorization.split(' ')[1]

            # Get JWT headers without verifying signature
            jwt_headers = jwt.get_unverified_header(token)
            if not jwt_headers.get('kid'):
                raise UnauthorizedError('Invalid token: missing key ID')

            logger.info(f"JWT headers: {jwt_headers}")

            return func(event, context)

        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid JWT token: {str(e)}")
            raise UnauthorizedError('Invalid token format')
        except pydantic.ValidationError as e:
            logger.error(f"Auth error: {str(e)}")
            raise UnauthorizedError("Unauthorized")

    return wrapper
