"""HTTP authentication classes."""

import logging
import time
from typing import Generator, Optional

import httpx

from ikclient.http.logging import get_logging_hooks

logger = logging.getLogger(__name__)


class ScaleJwtAuth(httpx.Auth):
    """Manage JWT token directly from ikscale dedicated endpoint.

    This permit to:
        * get a valid JWT from ikscale token API
        * avoid share sensible oauth client_id and client_secret

    But:
        * we can't (yet) get token using oauth flow
        * we can't (yet) refresh token using oauth flow
        * we have to use token API authentication
    """

    # Here, don't manage an async version, as
    # * httpx don't support auth_flow async version (for now)
    # * getting a valid JWT is a prerequisite, so even in async,
    #   need to keep this code blocking for all endpoint requests

    def __init__(self, scale_url: str, endpoint_url: str, token: str):
        """Initialize a new deployment auth class.

        Args:
            scale_url: Ikomia scale URL
            endpoint_url: deployment endpoint URL
            token: Token to authenticate
        """
        self.url = endpoint_url

        # Client to ikomia scale
        self.client = httpx.Client(
            base_url=scale_url,
            headers={"Authorization": f"Token {token}"},
            event_hooks=get_logging_hooks(logger, False),
        )

        self._expires_at: Optional[float] = None
        self._jwt: Optional[str] = None

    def jwt(self, force: bool = False) -> str:
        """Get a valid JWT for endpoint by creating or refreshing if needed.

        Args:
            force: force to get new token, even if current one is still valid

        Returns:
            A valid JWT token as str

        Raises:
            ValueError: when server response is invalid
        """
        # Will check if we have to renewal JWT
        if self._jwt is None or self._expires_at is None:
            logger.debug("No JWT exists for '%s', get one", self.url)
        elif self._expires_at < time.time():
            logger.debug("'%s' JWT token has expired, renew it", self.url)
        elif force:
            logger.debug("Force new '%s' JWT asked by user", self.url)
        else:
            # If here, current JWT exists and is still valid. Return it
            logger.debug("%s JWT token is still valid (expires at %s)", self.url, self._expires_at)
            return self._jwt

        # Call scale JWT endpoint to get token information
        response = self.client.get("/v1/projects/jwt/", params={"endpoint": self.url, "storage": True})
        response.raise_for_status()
        data = response.json()

        # Sanity check
        if "id_token" not in data or "expires_in" not in data:
            raise ValueError(f"Can't parse server response '{data}'")

        # Set JWT value
        self._jwt = f"Bearer {data['id_token']}"

        # Set expiry date. (Arbitrary) remove 1 minute to ensure avoid race conditions on token renewal
        self._expires_at = time.time() + data["expires_in"] - 60

        # Return fresh JWT
        return self._jwt

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        """Execute the httpx authentication flow.

        Args:
            request: An http request to set authorization headers

        Yields:
            Authorized request
        """
        request.headers["Authorization"] = self.jwt()
        yield request
