"""Enhance httpx logging by display lot of useful informations to debug ikomia scale deployment requests / responses."""

import logging

import httpx

# 'httpx' lib produce few uninteresting logs. Most of interesting one are done
#  on under the hood libs h11 / httpcore.
# But, it has *one* logger info when response.
# To avoid an unwanted log in the middle of nowhere, upraise log level to warn
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)


class HTTPLogger:
    """Expose sync and async method to log httpx Requests and Responses that can be used on httpx client event hooks."""

    def __init__(self, logger: logging.Logger):
        """Initialize new object with custom logger.

        Args:
            logger: A custom logger to use to log messages
        """
        self.logger = logger

    def log_request(self, request: httpx.Request):
        """Log request information.

        Args:
            request: A Request to log
        """
        # As only use debug, if logger level is upper, return immediatly
        if self.logger.level > logging.DEBUG:
            return

        self.logger.debug("HTTP Request %s '%s'", request.method, request.url)
        if request.headers:
            self.logger.debug(" with headers : %s", request.headers)
        if request.content:
            if len(request.content) > 2048:
                self.logger.debug(" with content : .... too long to be dumped ! ...")
            else:
                self.logger.debug(" with content : %s", request.content)

    async def async_log_request(self, request: httpx.Request):
        """Log request information, async version.

        Args:
            request: A Request to log
        """
        self.log_request(request)

    def _log_response_meta(self, response: httpx.Response):
        """Log response meta data.

        Args:
            response: A Response to log meta data
        """
        request = response.request

        # Log response meta
        self.logger.debug("HTTP Response to %s '%s'", request.method, request.url)
        self.logger.debug(" with code    : %d", response.status_code)
        self.logger.debug(" with headers : %s", response.headers)

    def _must_log_response_content(self, response: httpx.Response) -> bool:
        """Introspect and log about response content and return if whole content must be logged.

        Args:
            response: A response to log

        Returns:
            True if whole content must be logged, False otherwise
        """
        if "Content-Length" in response.headers:
            content_length = int(response.headers["Content-Length"])
            if content_length <= 0:
                self.logger.debug(" with no content")
            elif content_length > 10240:
                self.logger.debug(" with content : .... too long to be dumped ! ...")
            else:
                # If here, whole content can be logged
                return True
        else:
            self.logger.debug(" with unknown content")

        # In almost all cases, don't try to log content
        return False

    def log_response(self, response: httpx.Response):
        """Log response information.

        Args:
            response: A Response to log
        """
        # As only use debug, if logger level is upper, return immediatly
        if self.logger.level > logging.DEBUG:
            return

        # First log meta, then log about content
        self._log_response_meta(response)
        if self._must_log_response_content(response):
            # Ensure response was read
            response.read()
            self.logger.debug(" with content : %s", response.content)

    async def async_log_response(self, response: httpx.Response):
        """Log response information.

        Args:
            response: A Response to log
        """
        # As only use debug, if logger level is upper, return immediatly
        if self.logger.level > logging.DEBUG:
            return

        # First log meta, then log about content
        self._log_response_meta(response)
        if self._must_log_response_content(response):
            # Ensure response was read
            await response.aread()
            self.logger.debug(" with content : %s", response.content)


def get_logging_hooks(logger: logging.Logger, is_async: bool) -> dict:
    """Get httpx Client event hooks to log information about request and responses.

    Args:
        logger: A logger to use to log information about requests and responses
        is_async: True if must return async hooks version

    Returns:
        A dict with request and response hook, as expected by httpx.Client event_hooks
    """
    # Get logger object
    http_logger = HTTPLogger(logger)

    # Return hook, according to async param
    if is_async:
        return {"request": [http_logger.async_log_request], "response": [http_logger.async_log_response]}
    return {"request": [http_logger.log_request], "response": [http_logger.log_response]}
