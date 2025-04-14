"""Structlog middleware module."""

import logging
from typing import Optional

from starlette.types import ASGIApp, Receive, Scope, Send

import structlog

from fastapi_structlog.middleware.utils import find_request_info

try:
    from asgi_correlation_id.context import correlation_id
except ImportError:  # pragma: no cover
    from contextvars import ContextVar

    correlation_id = ContextVar('correlation_id', default=None)


class StructlogMiddleware:
    """Structlog middleware.

    Adds the request ID as the `request_id` key.
    """

    def __init__(
        self,
        app: ASGIApp,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """Initialization of the Structlog middleware.

        Args:
            app (ASGIApp): ASGI application
            logger (Optional[logging.Logger], optional): Logger. Defaults to None.
        """
        self.app = app
        self.logger = logger or logging.getLogger('api.error')

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:  # noqa: D102
        structlog.contextvars.clear_contextvars()

        if request_id := correlation_id.get():
            structlog.contextvars.bind_contextvars(request_id=request_id)

        if scope.get('type', '').startswith('http'):
            structlog.contextvars.bind_contextvars(request=find_request_info(scope))

        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            self.logger.exception(exc, exc_info=exc)  # noqa: TRY401
