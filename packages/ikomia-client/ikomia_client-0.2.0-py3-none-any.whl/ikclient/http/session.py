"""Deployment endpoint session, sync and async versions."""

import asyncio
import logging
import math
import random
import string
import time
from typing import Callable, List, Optional, Tuple, Union

import httpx
from yarl import URL

import ikclient.exceptions
import ikclient.http.exceptions
from ikclient.core.context import Context
from ikclient.core.results import Results
from ikclient.http.auth import ScaleJwtAuth
from ikclient.http.logging import get_logging_hooks

logger = logging.getLogger(__name__)


class PollerMixin:
    """A mixin for deployment endpoint results poller."""

    # How many times poll endpoint for result before giving up
    _max_polling_iterations = 100

    def _get_uuid(self, data: Union[dict, str]) -> str:
        """Get call UUID from deployment /api/run endpoint response.

        Args:
            data: Endpoint response

        Returns:
            Call UUID as str

        Raises:
            ValueError: when can't parse response
        """
        # If data is dict, uuid is member
        if isinstance(data, dict):
            return data["uuid"]

        # If data is str, it's plain uuid
        if isinstance(data, str):
            return data

        # If here, can't parse response
        raise ValueError(f"Can't extract UUID from a {type(data)}")

    def _next_polling_strategy(self, data: Optional[dict], count: int) -> Tuple[int, bool]:
        """Return information about next polling strategy.

        Args:
            data: Previous server response that embed (or not) polling advice
            count: Number of polling iteration

        Returns:
            A tuple with time to next polling, in ms and a bool if polling will be long (True) or short (Fale)

        Raises:
            ValueError: when can't parse response
        """
        polling_in_ms = None
        long = False

        if data is None or isinstance(data, str):
            # Legacy endpoint response. Don't support advice nor long
            long = False
        elif isinstance(data, dict):
            # Deployment give polling advice, extract infos
            polling_in_ms = data.get("next_poll_in", None)
            long = data.get("next_poll_long", False)
        else:
            # If here, can't parse response
            raise ValueError(f"Can't extract polling informations from a {type(data)}")

        if polling_in_ms is None:
            # If here, must be an old or serverless deployment, where no advice given
            #  and long polling not available.
            # Fallback to default strategy using a logistic function to get next polling time.
            polling_in_ms = int(20000 / (1.0 + math.exp(-0.3 * (count - 15))))
            long = False

        # Finally returns values
        return (polling_in_ms, long)

    def _get_progress_data(self, data: dict) -> dict:
        """Get data to give to 'on_progress' function from polling response.

        Args:
            data: Data returned by polling result query

        Returns:
            Data to give to 'on_progress' function as dict

        Raises:
            TypeError: when data type is not supported
        """
        # If legacy endpoint, without polling data
        if data is None or isinstance(data, str):
            return {"state": "PENDING", "eta": [None, None]}

        # If endpoint with polling advice, extract 'on_progress' data
        if isinstance(data, dict):
            return {"state": data["state"], "eta": data["eta"]}

        # If here, can't parse response
        raise TypeError(f"Can't get progress data from {type(data)}")

    def _on_progress(  # noqa: PLR0913, PLR0917
        self,
        run_id: Optional[str] = None,
        name: Optional[str] = None,
        uuid: Optional[str] = None,
        state: Optional[str] = None,
        eta: Optional[Tuple[Optional[int], Optional[int]]] = None,
        results: Optional[Results] = None,
    ):
        """Log task progress, default internal function.

        Args:
            run_id: A task unique id
            name: Name of running task
            uuid: Endpoint run uuid
            state: Endpoint run state (eg: PENDING, SUCCESS, ... )
            eta: A tuple with eta lower bound / upper bound
            results: Run results, if available
        """
        logger.debug(
            "%s/%s[%s] is %s (%s results), eta %s",
            run_id,
            uuid,
            name,
            state,
            "with" if results is not None else "no",
            eta,
        )


class ExtraSessionMixin:
    """A mixin to embed constants and functions to enhance Sessions (sync and async)."""

    # Extra headers for httpx.Client
    _session_headers = {"User-Agent": "ikclient"}

    # Default request timeout
    _default_timeout = 30.0

    def get_unique_id(self) -> str:
        """Get a unique id to track run steps through 'on_progress' function.

        Returns:
            A unique id, as str
        """
        return "".join(random.choices(string.hexdigits, k=12)).lower()

    def raise_for_status(self, response: httpx.Response):
        """Check response to give high valuable exception on deployment endpoint well known errors.

        Args:
            response: A response to check

        Raises:
            WorkflowFailedException: when a endpoint call run failed
        """
        # HTTP 520 is a special code when workflow run fail
        # Use a custom exception to extract rich information about failure
        if response.status_code == 520:
            request = response._request
            assert request is not None
            raise ikclient.http.exceptions.WorkflowFailedException(request, response)

        # Use common httpx function for all other errors
        response.raise_for_status()

    async def async_raise_for_status(self, response: httpx.Response):
        """Check response to give high valuable exception on deployment endpoint well known errors, async version.

        Args:
            response: A response to check
        """
        self.raise_for_status(response)


class Session(httpx.Client, ExtraSessionMixin, PollerMixin):
    """Sync session."""

    def __init__(self, url: URL, auth: ScaleJwtAuth):
        """Initialize a new session.

        Args:
            url: Deployment URL
            auth: Ikomia SCALE deployment authentication object
        """
        # Get logging event hooks, append one to check status
        event_hooks = get_logging_hooks(logger, False)
        event_hooks["response"].append(self.raise_for_status)

        super().__init__(
            base_url=str(url),
            http2=True,
            auth=auth,
            event_hooks=event_hooks,
            headers=self._session_headers,
            timeout=self._default_timeout,
        )

    def run_on(self, context: Context, inputs: List[dict], on_progress: Optional[Callable] = None) -> Results:
        """Run deployment.

        Args:
            context: A deployment run call context
            inputs: A list of image to run on
            on_progress: A callable to report call progress

        Returns:
            Run results

        Raises:
            httpx.HTTPError: when something get wrong on run call
            NoResultsException: when can't get run call results
        """
        # Get unique id to track task progress
        run_id = self.get_unique_id()

        # If progress is not defined, use internal one
        if on_progress is None:
            on_progress = self._on_progress

        # Get context payload and call endpoint
        payload = context.payload(inputs)
        on_progress(run_id=run_id, name=context.workflow.name, uuid=None, state="SENDING", eta=(None, None))
        try:
            response = self.put("/api/run", params={"advice": True}, json=payload)
        except httpx.HTTPError:
            # If something wrong happen when submit a run, report failure to progress
            on_progress(run_id=run_id, name=context.workflow.name, uuid=None, state="FAILURE", eta=(0, 0))
            # Then re-raise exception
            raise

        # Get data, and extract uuid to next calls
        data = response.json()
        uuid = self._get_uuid(data)

        # Iterate until getting results
        for index in range(self._max_polling_iterations):
            # Update progress
            on_progress(run_id=run_id, name=context.workflow.name, uuid=uuid, **(self._get_progress_data(data)))

            # Extract next polling info from last response and wait for next one
            polling_in_ms, long = self._next_polling_strategy(data, index)
            logger.debug("Will sleep for %i ms", polling_in_ms)
            time.sleep(polling_in_ms / 1000)

            # Try to get results
            try:
                response = self.get(f"/api/results/{uuid}", params={"advice": True, "long": long})
                data = response.json()
                # If status code is 200, results are available
                if response.status_code == 200:
                    if isinstance(data, dict) and "results" in data:
                        results = Results(uuid, inputs, data["results"])
                    else:  # Legacy endpoint response
                        results = data

                    on_progress(
                        run_id=run_id,
                        name=context.workflow.name,
                        uuid=uuid,
                        results=results,
                        **(self._get_progress_data(data)),
                    )
                    return results
            except httpx.HTTPError:
                # If something wrong happen when polling results, report failure to progress
                on_progress(run_id=run_id, name=context.workflow.name, uuid=uuid, state="FAILURE", eta=(0, 0))
                # Then re-raise exception
                raise

        # If here, fail to get polling result. Give up and raise exception
        raise ikclient.exceptions.NoResultsException()


class AsyncSession(httpx.AsyncClient, ExtraSessionMixin, PollerMixin):
    """Async session."""

    # Maximum number of concurrent calls
    concurrent_call_limit = 10

    def __init__(self, url: URL, auth: ScaleJwtAuth):
        """Initialize a new async session.

        Args:
            url: Deployment URL
            auth: Ikomia SCALE deployment authentication object
        """
        # Get logging event hooks, append one to check status
        event_hooks = get_logging_hooks(logger, True)
        event_hooks["response"].append(self.async_raise_for_status)

        super().__init__(
            base_url=format(url),
            http2=True,
            auth=auth,
            event_hooks=event_hooks,
            headers=self._session_headers,
            timeout=self._default_timeout,
        )
        # Instance semaphore for current event loop
        self.semaphore = asyncio.Semaphore(5)

    def set_concurrent_call(self, count: int):
        """Set the maximum concurrent calls.

        Args:
            count: max concurrent calls when using asyncio tasks

        Raises:
            ValueError: when trying to set a value greater than concurrent_call_limit
        """
        if count > self.concurrent_call_limit:
            raise ValueError(f"Can't set more than {self.concurrent_call_limit} concurrent call")
        self.semaphore = asyncio.Semaphore(count)

    async def run_on(self, context: Context, inputs: List[dict], on_progress: Optional[Callable] = None) -> Results:
        """Run deployment.

        Args:
            context: A deployment run call context
            inputs: A list of image to run on
            on_progress: A callable to report call progress

        Returns:
            Run results

        Raises:
            httpx.HTTPError: when something get wrong on run call
            NoResultsException: when can't get run call results
        """
        # Get unique id to track task progress
        run_id = self.get_unique_id()

        # If progress is not defined, use internal one
        if on_progress is None:
            on_progress = self._on_progress

        # Get context payload
        payload = context.payload(inputs)

        # First call on_progress function outside semaphore
        on_progress(run_id=run_id, name=context.workflow.name, uuid=None, state="BLOCKING", eta=(None, None))

        async with self.semaphore:
            # Send run call
            try:
                on_progress(run_id=run_id, name=context.workflow.name, uuid=None, state="SENDING", eta=(None, None))
                response = await self.put("/api/run", params={"advice": True}, json=payload)
            except httpx.HTTPError:
                # If something wrong happen when submit a run, report failure to progress
                on_progress(run_id=run_id, name=context.workflow.name, uuid=None, state="FAILURE", eta=(0, 0))
                # Then re-raise exception
                raise

            # Get data, and extract uuid to next calls
            data = response.json()
            uuid = self._get_uuid(data)

            # Iterate until getting results
            for index in range(self._max_polling_iterations):
                # Update progress
                on_progress(run_id=run_id, name=context.workflow.name, uuid=uuid, **(self._get_progress_data(data)))

                # Extract next polling infos from last response and wait for next one
                polling_in_ms, long = self._next_polling_strategy(data, index)
                logger.debug("Will sleep for %i ms", polling_in_ms)
                await asyncio.sleep(polling_in_ms / 1000)

                # Try to get for results
                try:
                    response = await self.get(f"/api/results/{uuid}", params={"advice": True, "long": long})
                    data = response.json()
                    # If status code is 200, results are available
                    if response.status_code == 200:
                        if isinstance(data, dict) and "results" in data:
                            results = Results(uuid, inputs, data["results"])
                        else:  # Legacy endpoint response
                            results = data
                        on_progress(
                            run_id=run_id,
                            name=context.workflow.name,
                            uuid=uuid,
                            results=results,
                            **(self._get_progress_data(data)),
                        )
                        return results
                except httpx.HTTPError:
                    # If something wrong happen when polling results, report failure to progress
                    on_progress(run_id=run_id, name=context.workflow.name, uuid=uuid, state="FAILURE", eta=(0, 0))
                    # Then re-raise exception
                    raise

            # If here, fail to get polling result. Give up and raise exception
            raise ikclient.exceptions.NoResultsException()
