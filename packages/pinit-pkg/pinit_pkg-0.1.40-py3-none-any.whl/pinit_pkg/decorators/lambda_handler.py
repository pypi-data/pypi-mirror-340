from functools import wraps
from typing import Any, Callable, Dict
from loguru import logger

from pinit_pkg.errors import UnsupportedMediaTypeError, BadRequestError, NotFoundError, UnauthorizedError
from pinit_pkg.request import parse_headers
from pinit_pkg.responses import handle_response, response_error



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
