"""Ikomia SCALE deployment API client."""

import asyncio
import json
import logging
import mimetypes
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Optional, Union, cast

import fsspec
from yarl import URL

import ikclient.http.auth
from ikclient.core.context import Context
from ikclient.core.io import BaseTaskIO, ImageIO, StorageObjectIO, TaskIO
from ikclient.core.results import Results
from ikclient.core.workflow import Workflow
from ikclient.exceptions import CannotInferPathDataTypeException
from ikclient.http.session import AsyncSession, Session
from ikclient.storage.client import AsyncStorageClient, BaseStorageClient, StorageClient, StorageObject

logger = logging.getLogger(__name__)


class BaseClient(ABC):
    """Base client for Ikomia SCALE deployment API."""

    def __init__(self, url: Union[str, URL], token: Optional[str] = None):
        """Initialize deployment API client.

        Args:
            url: Ikomia SCALE deployment endpoint URL.
            token: API token. Defaults to IKOMIA_TOKEN environment variable.
        """
        self.url = URL(url)
        scale_url = URL(os.getenv("IKOMIA_URL", "https://scale.ikomia.ai"))

        # Initialize auth
        token = token if token is not None else os.getenv("IKOMIA_TOKEN")
        assert isinstance(token, str)

        self._auth = ikclient.http.auth.ScaleJwtAuth(str(scale_url), str(self.url), token)

        # Cache workflow
        self._workflow: Optional[Workflow] = None

    @property
    @abstractmethod
    def storage(self) -> BaseStorageClient:
        """Return a well initialized storage client."""
        pass

    def _get_data_type_from_path(self, path: str, data_type: Optional[str] = None) -> tuple[str, Optional[str]]:
        path_mime, _ = mimetypes.guess_type(path)

        if data_type is not None:
            return data_type, path_mime

        if path_mime is None:
            raise CannotInferPathDataTypeException()
        if path_mime.startswith("image/"):
            return "image", path_mime
        if path_mime.startswith("video/"):
            return "video", path_mime

        raise CannotInferPathDataTypeException()

    def _get_raw_inputs(self, *inputs: Union[BaseTaskIO, Results, dict]) -> list[dict]:
        raw_inputs = []
        for input_data in inputs:
            if isinstance(input_data, BaseTaskIO):
                raw_inputs.append(input_data.raw)
            elif isinstance(input_data, Results):
                raw_inputs.extend(input_data._outputs)
            elif isinstance(input_data, dict):
                raw_inputs.append(input_data)
            else:
                raise TypeError(f"Unsupported input type: {type(input_data)}")
        return raw_inputs

    def _create_storage_input_from_object(
        self, obj: StorageObject, *, data_type: Optional[str] = None
    ) -> StorageObjectIO:
        if data_type is None:
            if not obj["content_type"]:
                raise CannotInferPathDataTypeException()
            if obj["content_type"].startswith("image/"):
                data_type = "image"
            elif obj["content_type"].startswith("video/"):
                data_type = "video"
            else:
                raise CannotInferPathDataTypeException()

        return StorageObjectIO(
            {
                "storage_object": {
                    "url": str(self.storage.scalefs_url / "v1/objects/" % {"uid": obj["uid"]}),
                    "data_type": data_type,
                }
            }
        )


class Client(BaseClient):
    """Client for Ikomia SCALE deployment API."""

    def __init__(self, url: Union[str, URL], token: Optional[str] = None):
        """Initialize deployment API client.

        Args:
            url: Ikomia SCALE deployment endpoint URL.
            token: API token. Defaults to IKOMIA_TOKEN environment variable.
        """
        super().__init__(url, token)
        self._session: Optional[Session] = None
        self._storage: Optional[StorageClient] = None

    @property
    def session(self) -> Session:
        """Return a well initialized session.

        Returns:
            Session: HTTP client session.
        """
        if self._session is None:
            self._session = Session(self.url, self._auth)
        return self._session

    @property
    def storage(self) -> StorageClient:
        """Return a well initialized storage client.

        Returns:
            StorageClient: Storage client.
        """
        if self._storage is None:
            self._storage = StorageClient(self.url, _auth=self._auth)
        return self._storage

    def close(self):
        """Close the HTTP client session."""
        if self._session is not None:
            self._session.close()

    def __enter__(self) -> "Client":
        """Enter context manager.

        Returns:
            Client: Self instance.
        """
        logger.debug("Open session on %s", self.url)
        _ = self.session
        return self

    def __exit__(self, *_):
        """Exit context manager and close client."""
        logger.debug("Close session on %s", self.url)
        self.close()

    def get_workflow(self) -> Workflow:
        """Get deployment workflow.

        Returns:
            Workflow: Deployment workflow.
        """
        if self._workflow is None:
            response = self.session.get("/workflow")
            self._workflow = Workflow(response.json())
        return self._workflow

    def build_context(self) -> Context:
        """Create a new context for this deployment endpoint.

        Returns:
            Context: A properly initialized context.
        """
        workflow = self.get_workflow()
        return Context(workflow)

    def create_input(
        self,
        path: Union[str, Path],
        *,
        data_type: Optional[str] = None,
        save_temporary=False,
        storage_options: Optional[dict] = None,
    ) -> BaseTaskIO:
        """Get deployment input from a file path.

        Args:
            path: Path to the input file. Support fsspec paths (e.g. "s3://bucket/file").
            data_type: Input type (e.g. "image", "video").
                If not provided, inferred from file extension.
            save_temporary: If True, upload the data to SCALE storage.
                Note: Video inputs are always uploaded to SCALE storage.
            storage_options: Options for fsspec file system.
                https://filesystem-spec.readthedocs.io/en/latest

        Returns:
            BaseTaskIO: Object as deployment input.
        """
        fs, _, [path] = fsspec.get_fs_token_paths(path, storage_options=storage_options)
        fs = cast(fsspec.AbstractFileSystem, fs)

        data_type, path_mime = self._get_data_type_from_path(str(path), data_type=data_type)

        with fs.open(path, "rb") as file:
            if save_temporary or data_type == "video":
                uploaded_obj = self.storage.put(file.read(), content_type=path_mime)
                return self._create_storage_input_from_object(uploaded_obj, data_type=data_type)

            if data_type == "image":
                return ImageIO.create(file.read())

            return TaskIO(json.loads(file.read().decode("utf-8")))

    def create_storage_input(self, path: str, *, data_type: Optional[str] = None) -> StorageObjectIO:
        """Get deployment input from a storage object path.

        Args:
            path: Path to the object in SCALE storage.
            data_type: Input type (e.g. "image", "video").
                If not provided, inferred from content type.

        Returns:
            StorageObjectIO: Object as deployment input.
        """
        obj = self.storage.get(path)
        return self._create_storage_input_from_object(obj, data_type=data_type)

    def create_storage_input_from_uid(self, uid: str, *, data_type: Optional[str] = None) -> StorageObjectIO:
        """Get deployment input from a storage object UID.

        Args:
            uid: Object unique identifier.
            data_type: Input type (e.g. "image", "video").
                If not provided, inferred from content type.

        Returns:
            StorageObjectIO: Object as deployment input.
        """
        obj = self.storage.get_by_uid(uid)
        return self._create_storage_input_from_object(obj, data_type=data_type)

    def run(
        self,
        *inputs: Union[str, Path, BaseTaskIO, Results, dict],
        parameters: Optional[dict[str, object]] = None,
        on_progress: Optional[Callable] = None,
    ) -> Results:
        """Run the deployment's final task.

        Args:
            *inputs: Input data. Can be a path, a BaseTaskIO, a Results object, or a serialized JSON input.
            parameters: Task parameters.
            on_progress: Callback for progress reporting.

        Returns:
            Results: Task execution results.
        """
        # Get final task from workflow
        workflow = self.get_workflow()
        task_name = workflow.get_first_final_task_name()

        # Then call run_task
        return self.run_task(task_name, *inputs, parameters=parameters, on_progress=on_progress)

    def run_task(
        self,
        task_name: str,
        *inputs: Union[str, Path, BaseTaskIO, Results, dict],
        parameters: Optional[dict[str, object]] = None,
        on_progress: Optional[Callable] = None,
    ) -> Results:
        """Run a specific task in the deployment.

        Args:
            task_name: Name of the task to run.
            *inputs: Input data. Can be a path, a BaseTaskIO, a Results object, or a serialized JSON input.
            parameters: Task parameters.
            on_progress: Callback for progress reporting.

        Returns:
            Results: Task execution results.
        """
        # Get context
        context = self.build_context()

        # Add parameters if needed
        if parameters:
            context.set_parameters(task_name, parameters)

        # Add default output
        context.add_output(task_name)

        # Run context
        return self.run_on(context, *inputs, on_progress=on_progress)

    def run_on(
        self,
        context: Context,
        *inputs: Union[str, Path, BaseTaskIO, Results, dict],
        on_progress: Optional[Callable] = None,
    ) -> Results:
        """Run with a specific context.

        Args:
            context: Execution context with parameters and outputs configuration.
            *inputs: Input data. Can be a path, a BaseTaskIO, a Results object, or a serialized JSON input.
            on_progress: Callback for progress reporting.

        Returns:
            Results: Task execution results.
        """
        # Convert processed inputs to raw inputs
        raw_inputs = self._get_raw_inputs(
            *[self.create_input(inp) if isinstance(inp, (str, Path)) else inp for inp in inputs]
        )

        return self.session.run_on(context, raw_inputs, on_progress=on_progress)


class AsyncClient(BaseClient):
    """Async client for Ikomia SCALE deployment API."""

    def __init__(self, url: Union[str, URL], token: Optional[str] = None):
        """Initialize async deployment API client.

        Args:
            url: Ikomia SCALE deployment endpoint URL.
            token: API token. Defaults to IKOMIA_TOKEN environment variable.
        """
        super().__init__(url, token)
        self._session: Optional[AsyncSession] = None
        self._storage: Optional[AsyncStorageClient] = None

    @property
    def session(self) -> AsyncSession:
        """Return a well initialized session.

        Returns:
            AsyncSession: Async HTTP client session.
        """
        if self._session is None:
            self._session = AsyncSession(self.url, self._auth)
        return self._session

    @property
    def storage(self) -> AsyncStorageClient:
        """Return a well initialized storage client.

        Returns:
            AsyncStorageClient: Async storage client.
        """
        if self._storage is None:
            self._storage = AsyncStorageClient(self.url, _auth=self._auth)
        return self._storage

    async def aclose(self):
        """Close the HTTP client session."""
        if self._session is not None:
            await self._session.aclose()

    async def __aenter__(self) -> "AsyncClient":
        """Enter async context manager.

        Returns:
            AsyncClient: Self instance.
        """
        logger.debug("Open session on %s", self.url)
        _ = self.session
        return self

    async def __aexit__(self, *_):
        """Exit async context manager and close client."""
        logger.debug("Close session on %s", self.url)
        await self.aclose()

    async def get_workflow(self) -> Workflow:
        """Get deployment workflow.

        Returns:
            Workflow: Deployment workflow.
        """
        if self._workflow is None:
            response = await self.session.get("/workflow")
            self._workflow = Workflow(response.json())
        return self._workflow

    async def build_context(self) -> Context:
        """Create a new context for this deployment endpoint.

        Returns:
            Context: A properly initialized context.
        """
        workflow = await self.get_workflow()
        return Context(workflow)

    async def create_input(
        self,
        path: Union[str, Path],
        *,
        data_type: Optional[str] = None,
        save_temporary=False,
        storage_options: Optional[dict] = None,
    ) -> BaseTaskIO:
        """Get deployment input from a file path.

        Args:
            path: Path to the input file. Support fsspec paths (e.g. "s3://bucket/file").
            data_type: Input type (e.g. "image", "video").
                If not provided, inferred from file extension.
            save_temporary: If True, upload the data to SCALE storage.
                Note: Video inputs are always uploaded to SCALE storage.
            storage_options: Options for fsspec file system.
                https://filesystem-spec.readthedocs.io/en/latest

        Returns:
            BaseTaskIO: Object as deployment input.
        """
        fs, _, [path] = fsspec.get_fs_token_paths(path, storage_options=storage_options)
        fs = cast(fsspec.AbstractFileSystem, fs)

        data_type, path_mime = self._get_data_type_from_path(str(path), data_type=data_type)

        with fs.open(path, "rb") as file:
            if save_temporary or data_type == "video":
                uploaded_obj = await self.storage.put(file.read(), content_type=path_mime)
                return self._create_storage_input_from_object(uploaded_obj, data_type=data_type)

            if data_type == "image":
                return ImageIO.create(file.read())

            return TaskIO(json.loads(file.read().decode("utf-8")))

    async def create_storage_input(self, path: str, *, data_type: Optional[str] = None) -> StorageObjectIO:
        """Get deployment input from a storage object path.

        Args:
            path: Path to the object in SCALE storage.
            data_type: Input type (e.g. "image", "video").
                If not provided, inferred from content type.

        Returns:
            StorageObjectIO: Object as deployment input.
        """
        obj = await self.storage.get(path)
        return self._create_storage_input_from_object(obj, data_type=data_type)

    async def create_storage_input_from_uid(self, uid: str, *, data_type: Optional[str] = None) -> StorageObjectIO:
        """Get deployment input from a storage object UID.

        Args:
            uid: Object unique identifier.
            data_type: Input type (e.g. "image", "video").
                If not provided, inferred from content type.

        Returns:
            StorageObjectIO: Object as deployment input.
        """
        obj = await self.storage.get_by_uid(uid)
        return self._create_storage_input_from_object(obj, data_type=data_type)

    async def run(
        self,
        *inputs: Union[str, Path, BaseTaskIO, Results, dict],
        parameters: Optional[dict[str, object]] = None,
        on_progress: Optional[Callable] = None,
    ) -> Results:
        """Run the deployment's final task.

        Args:
            *inputs: Input data. Can be a path, a BaseTaskIO, a Results object, or a serialized JSON input.
            parameters: Task parameters.
            on_progress: Callback for progress reporting.

        Returns:
            Results: Task execution results.
        """
        # Get final task from workflow
        workflow = await self.get_workflow()
        task_name = workflow.get_first_final_task_name()

        # Then call run_task
        return await self.run_task(task_name, *inputs, parameters=parameters, on_progress=on_progress)

    async def run_task(
        self,
        task_name: str,
        *inputs: Union[str, Path, BaseTaskIO, Results, dict],
        parameters: Optional[dict[str, object]] = None,
        on_progress: Optional[Callable] = None,
    ) -> Results:
        """Run a specific task in the deployment.

        Args:
            task_name: Name of the task to run.
            *inputs: Input data. Can be a path, a BaseTaskIO, a Results object, or a serialized JSON input.
            parameters: Task parameters.
            on_progress: Callback for progress reporting.

        Returns:
            Results: Task execution results.
        """
        # Get context
        context = await self.build_context()

        # Add parameters if needed
        if parameters:
            context.set_parameters(task_name, parameters)

        # Add default output
        context.add_output(task_name)

        # Run context
        return await self.run_on(context, *inputs, on_progress=on_progress)

    async def run_on(
        self,
        context: Context,
        *inputs: Union[str, Path, BaseTaskIO, Results, dict],
        on_progress: Optional[Callable] = None,
    ) -> Results:
        """Run with a specific context.

        Args:
            context: Execution context with parameters and outputs configuration.
            *inputs: Input data. Can be a path, a BaseTaskIO, a Results object, or a serialized JSON input.
            on_progress: Callback for progress reporting.

        Returns:
            Results: Task execution results.
        """

        async def _identity(x: Union[BaseTaskIO, Results, dict]) -> Union[BaseTaskIO, Results, dict]:
            return x

        loaded_inputs = await asyncio.gather(
            *[self.create_input(inp) if isinstance(inp, (str, Path)) else _identity(inp) for inp in inputs]
        )
        raw_inputs = self._get_raw_inputs(*loaded_inputs)

        return await self.session.run_on(context, raw_inputs, on_progress=on_progress)
