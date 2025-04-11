"""HTTP custom exceptions."""

import httpx

import ikclient.exceptions


class WorkflowFailedException(httpx.HTTPStatusError, ikclient.exceptions.IkClientBaseException):
    """When workflow fail to run and return rich content about error (ie HTTP 520 + body json error)."""

    def __init__(self, request: httpx.Request, response: httpx.Response):
        """Initialize a new exception.

        Args:
            request: HTTP request that fail
            response: HTTP Response with error details
        """
        # Try to extract error message from json body
        content = response.json()
        message = content.get("message", "Workflow run failed")

        # Initialize parent exception
        super().__init__(message, request=request, response=response)
