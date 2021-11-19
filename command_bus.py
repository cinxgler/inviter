import logging
import typing as t

from pymessagebus._commandbus import CommandBus  # type: ignore
from pymessagebus.api import CommandHandlerNotFound  # type: ignore
from pymessagebus.middleware.logger import (  # type: ignore
    LoggingMiddlewareConfig,
    get_logger_middleware,
)

logger = logging.getLogger("message_bus")
logging_middleware_config = LoggingMiddlewareConfig(
    mgs_received_level=logging.INFO,
    mgs_succeeded_level=logging.INFO,
    mgs_failed_level=logging.CRITICAL,
)
logging_middleware = get_logger_middleware(logger, logging_middleware_config)

_DEFAULT_COMMAND_BUS = CommandBus(middlewares=[logging_middleware])

# Public API:
# This is our handy decorator:
def register_handler(message_class: type):
    def decorator(handler: t.Callable):
        _DEFAULT_COMMAND_BUS.add_handler(message_class, handler)
        return handler

    return decorator


# And those are aliases to our "default" singleton instance:
# pylint: disable=invalid-name
add_handler = _DEFAULT_COMMAND_BUS.add_handler
handle = _DEFAULT_COMMAND_BUS.handle
has_handler_for = _DEFAULT_COMMAND_BUS.has_handler_for
