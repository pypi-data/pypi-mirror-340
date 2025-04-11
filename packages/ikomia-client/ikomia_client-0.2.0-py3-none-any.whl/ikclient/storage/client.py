"""Ikomia SCALE storage API client."""

import datetime
import mimetypes
import os
from abc import ABC
from contextlib import asynccontextmanager, contextmanager
from typing import List, Literal, Optional, Union, cast

import httpx
from typing_extensions import NotRequired, TypedDict
from yarl import URL

import ikclient.http.auth


class StorageObject(TypedDict):
    """Metadata of a stored object."""

    uid: str
    path: NotRequired[str]
    download_url: NotRequired[str]
    is_directory_archive: bool
    content_type: NotRequired[str]
    sha256: NotRequired[str]
    size: NotRequired[int]
    created_at: NotRequired[str]


class BaseStorageClient(ABC):
    """Base client for Ikomia SCALE storage API."""

    def __init__(
        self,
        url: Union[str, URL],
        token: Optional[str] = None,
        *,
        _auth: Optional[ikclient.http.auth.ScaleJwtAuth] = None,
    ):
        """Initialize storage API client.

        Args:
            url: Ikomia SCALE deployment endpoint URL.
            token: API token. Defaults to IKOMIA_TOKEN environment variable.
        """
        scale_url = URL(os.getenv("IKOMIA_URL", "https://scale.ikomia.ai"))
        self.scalefs_url = URL(os.getenv("IKOMIA_SCALEFS_URL", "https://scalefs.ikomia.ai"))

        # Init auth
        if _auth is None:
            token = token if token is not None else os.getenv("IKOMIA_TOKEN")
            assert isinstance(token, str)
            self._auth = ikclient.http.auth.ScaleJwtAuth(str(scale_url), str(url), token)
        else:
            self._auth = _auth

    def _get_object_route(self, path: Optional[str] = None) -> str:
        route = URL("/v1/objects/")
        if path:
            route /= path.removeprefix("/")

        return str(route)

    def _handle_response_status(self, response: httpx.Response) -> None:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 409:
                raise FileExistsError(e.response.json()["detail"]) from e
            elif e.response.status_code == 404:
                raise FileNotFoundError(e.response.json()["detail"]) from e

            raise

    def _infer_content_type(self, path: Optional[str] = None, content: Optional[Union[str, bytes]] = None) -> str:
        path_content_type = None
        if path:
            # Try to infer content type from file extension
            path_content_type, _ = mimetypes.guess_type(path)

        if path_content_type:
            return path_content_type

        if isinstance(content, str):
            return "text/plain"

        return "application/octet-stream"

    def _get_expiration_date(self, expire_in: Union[datetime.timedelta, int]) -> datetime.datetime:
        if isinstance(expire_in, int):
            expire_in = datetime.timedelta(seconds=expire_in)

        return datetime.datetime.now().astimezone() + expire_in


class StorageClient(BaseStorageClient):
    """Client for Ikomia SCALE storage API."""

    def __init__(
        self,
        url: Union[str, URL],
        token: Optional[str] = None,
        *,
        _auth: Optional[ikclient.http.auth.ScaleJwtAuth] = None,
    ):
        """Initialize storage API client.

        Args:
            url: Ikomia SCALE deployment endpoint URL.
            token: API token. Defaults to IKOMIA_TOKEN environment variable.
        """
        super().__init__(url, token, _auth=_auth)
        self.client = httpx.Client(
            base_url=str(self.scalefs_url),
            auth=self._auth,
            headers={"User-Agent": "ikclient"},
            timeout=httpx.Timeout(30, write=None),
        )

    def close(self):
        """Close the HTTP client session."""
        self.client.close()

    def __enter__(self) -> "StorageClient":
        """Enter context manager.

        Returns:
            Self instance.
        """
        return self

    def __exit__(self, *_):
        """Exit context manager and close client."""
        self.close()

    def _fetch_objects(
        self, path: Optional[str] = None, params: Optional[dict] = None, limit: Optional[int] = None
    ) -> List[StorageObject]:
        if params is None:
            params = {}

        objects: List[StorageObject] = []
        page = 1

        while True:
            response = self.client.get(self._get_object_route(path), params={**params, "page": page})
            self._handle_response_status(response)
            json = response.json()

            objects.extend(json["results"])

            if not json["next"]:
                break
            page += 1

            if limit and len(objects) >= limit:
                objects = objects[:limit]
                break

        return objects

    def get(self, path: str) -> StorageObject:
        """Get object metadata by path.

        Args:
            path: Path to the object.

        Returns:
            StorageObject: Object metadata.

        Raises:
            FileNotFoundError: If object not found.
        """
        objects = self._fetch_objects(path, params={"exact": True}, limit=1)

        if len(objects) == 0:
            raise FileNotFoundError(f"Object not found: {path}")

        return objects[0]

    def get_by_uid(self, uid: str) -> StorageObject:
        """Get object metadata by UID.

        Args:
            uid: Object unique identifier.

        Returns:
            StorageObject: Object metadata.

        Raises:
            FileNotFoundError: If object not found.
        """
        objects = self._fetch_objects(params={"uid": uid}, limit=1)

        if len(objects) == 0:
            raise FileNotFoundError(f"Object not found: {uid}")

        return objects[0]

    def list(self, path: Optional[str] = None) -> List[StorageObject]:
        """List objects with path prefix.

        Args:
            path: Prefix path to filter objects. If None, lists all objects.

        Returns:
            List[StorageObject]: Matching objects metadata.
        """
        return self._fetch_objects(path)

    def list_by_sha256(self, sha256: str) -> List[StorageObject]:
        """List objects with matching SHA256 hash.

        Args:
            sha256: Hash to filter objects by.

        Returns:
            List[StorageObject]: Matching objects metadata.
        """
        return self._fetch_objects(params={"sha256": sha256})

    def put(
        self,
        content: Union[str, bytes],
        path: Optional[str] = None,
        *,
        content_type: Optional[str] = None,
        is_directory_archive=False,
        overwrite=False,
    ) -> StorageObject:
        """Upload content to storage.

        Args:
            content: Content to upload (text or bytes).
            path: Destination path. If None, creates a temporary object.
            content_type: Content type of uploaded data.
                If None, inferred from file extension or defaults to "text/plain" or "application/octet-stream".
            is_directory_archive: Whether content is a directory archive.
            overwrite: Whether to overwrite existing object.

        Returns:
            StorageObject: Uploaded object metadata.
        """
        response = self.client.request(
            "PUT" if path and overwrite else "POST",
            self._get_object_route(path),
            data={
                "is_directory_archive": str(is_directory_archive).lower(),
            },
            files={"file": (None, content, content_type or self._infer_content_type(path, content))},
        )
        self._handle_response_status(response)

        return cast(StorageObject, response.json())

    def copy(self, source: dict[Literal["uid"], str], path: Optional[str] = None, *, overwrite=False) -> StorageObject:
        """Copy object to new location.

        Args:
            source: Source object to copy.
            path: Destination path. If None, creates a temporary object.
            overwrite: Whether to overwrite existing object.

        Returns:
            StorageObject: Copied object metadata.
        """
        # Check if source is a valid object
        self.get_by_uid(source["uid"])

        response = self.client.request(
            "PUT" if path and overwrite else "POST",
            self._get_object_route(path),
            data={
                "copy_from": source["uid"],
            },
            files={"file": (None, b"", None)},  # Empty file to send query as multipart/form-data
        )
        self._handle_response_status(response)

        return cast(StorageObject, response.json())

    def delete(self, path: str, *, exact=False) -> None:
        """Delete object(s) by path.

        Args:
            path: Path to the object to delete.
            exact: If True, only delete exact path match.
                If False, delete all objects with this path prefix.
        """
        response = self.client.delete(self._get_object_route(path), params={"exact": exact})
        self._handle_response_status(response)

    def get_presigned_download_url(
        self,
        source: dict[Literal["uid"], str],
        *,
        expire_in: Union[datetime.timedelta, int] = datetime.timedelta(hours=1),
    ) -> str:
        """Generate pre-signed download URL for an object.

        Args:
            source: Source object.
            expire_in: URL expiration time. Defaults to 1 hour.

        Returns:
            str: Pre-signed download URL.
        """
        response = self.client.put(
            str(URL("/v1/presigned-urls/download/") / source["uid"]),
            data={
                "expire_at": self._get_expiration_date(expire_in).isoformat(),
            },
        )
        self._handle_response_status(response)

        return response.json()["presigned_download_url"]

    @contextmanager
    def read(self, obj: dict[Literal["uid"], str], *, stream=False):
        """Read the response content.

        Args:
            obj: Object to read.
            stream: If True, return a streaming response.

        Yields:
            httpx.Response: Response object.
        """
        download_url = self.get_by_uid(obj["uid"])["download_url"]

        if stream:
            with self.client.stream("GET", download_url) as response:
                self._handle_response_status(response)
                yield response

            return

        yield self.client.get(download_url)


class AsyncStorageClient(BaseStorageClient):
    """Async client for Ikomia SCALE storage API."""

    def __init__(
        self,
        url: Union[str, URL],
        token: Optional[str] = None,
        *,
        _auth: Optional[ikclient.http.auth.ScaleJwtAuth] = None,
    ):
        """Initialize async storage API client.

        Args:
            url: Ikomia SCALE deployment endpoint URL.
            token: API token. Defaults to IKOMIA_TOKEN environment variable.
        """
        super().__init__(url, token, _auth=_auth)
        self.client = httpx.AsyncClient(
            base_url=str(self.scalefs_url),
            auth=self._auth,
            headers={"User-Agent": "ikclient"},
            timeout=httpx.Timeout(30, write=None),
        )

    async def aclose(self):
        """Close the HTTP client session."""
        await self.client.aclose()

    async def __aenter__(self) -> "AsyncStorageClient":
        """Enter async context manager.

        Returns:
            Self instance.
        """
        return self

    async def __aexit__(self, *_):
        """Exit async context manager and close client."""
        await self.aclose()

    async def _fetch_objects(
        self, path: Optional[str] = None, params: Optional[dict] = None, limit: Optional[int] = None
    ) -> List[StorageObject]:
        if params is None:
            params = {}

        objects: List[StorageObject] = []
        page = 1

        while True:
            response = await self.client.get(self._get_object_route(path), params={**params, "page": page})
            self._handle_response_status(response)
            json = response.json()

            objects.extend(json["results"])

            if not json["next"]:
                break
            page += 1

            if limit and len(objects) >= limit:
                objects = objects[:limit]
                break

        return objects

    async def get(self, path: str) -> StorageObject:
        """Get object metadata by path.

        Args:
            path: Path to the object.

        Returns:
            StorageObject: Object metadata.

        Raises:
            FileNotFoundError: If object not found.
        """
        objects = await self._fetch_objects(path, params={"exact": True}, limit=1)

        if len(objects) == 0:
            raise FileNotFoundError(f"Object not found: {path}")

        return objects[0]

    async def get_by_uid(self, uid: str) -> StorageObject:
        """Get object metadata by UID.

        Args:
            uid: Object unique identifier.

        Returns:
            StorageObject: Object metadata.

        Raises:
            FileNotFoundError: If object not found.
        """
        objects = await self._fetch_objects(params={"uid": uid}, limit=1)

        if len(objects) == 0:
            raise FileNotFoundError(f"Object not found: {uid}")

        return objects[0]

    async def list(self, path: Optional[str] = None) -> List[StorageObject]:
        """List objects with path prefix.

        Args:
            path: Prefix path to filter objects. If None, lists all objects.

        Returns:
            List[StorageObject]: Matching objects metadata.
        """
        return await self._fetch_objects(path)

    async def list_by_sha256(self, sha256: str) -> List[StorageObject]:
        """List objects with matching SHA256 hash.

        Args:
            sha256: Hash to filter objects by.

        Returns:
            List[StorageObject]: Matching objects metadata.
        """
        return await self._fetch_objects(params={"sha256": sha256})

    async def put(
        self,
        content: Union[str, bytes],
        path: Optional[str] = None,
        *,
        content_type: Optional[str] = None,
        is_directory_archive=False,
        overwrite=False,
    ) -> StorageObject:
        """Upload content to storage.

        Args:
            content: Content to upload (text or bytes).
            path: Destination path. If None, creates a temporary object.
            content_type: Content type of uploaded data.
                If None, inferred from file extension or defaults to "text/plain" or "application/octet-stream".
            is_directory_archive: Whether content is a directory archive.
            overwrite: Whether to overwrite existing object.

        Returns:
            StorageObject: Uploaded object metadata.
        """
        response = await self.client.request(
            "PUT" if path and overwrite else "POST",
            self._get_object_route(path),
            data={
                "is_directory_archive": str(is_directory_archive).lower(),
            },
            files={"file": (None, content, content_type or self._infer_content_type(path, content))},
        )
        self._handle_response_status(response)

        return cast(StorageObject, response.json())

    async def copy(
        self, source: dict[Literal["uid"], str], path: Optional[str] = None, *, overwrite=False
    ) -> StorageObject:
        """Copy object to new location.

        Args:
            source: Source object to copy.
            path: Destination path. If None, creates a temporary object.
            overwrite: Whether to overwrite existing object.

        Returns:
            StorageObject: Copied object metadata.
        """
        # Check if source is a valid object
        await self.get_by_uid(source["uid"])

        response = await self.client.request(
            "PUT" if path and overwrite else "POST",
            self._get_object_route(path),
            data={
                "copy_from": source["uid"],
            },
            files={"file": (None, b"", None)},  # Empty file to send query as multipart/form-data
        )
        self._handle_response_status(response)

        return cast(StorageObject, response.json())

    async def delete(self, path: str, *, exact=False) -> None:
        """Delete object(s) by path.

        Args:
            path: Path to the object to delete.
            exact: If True, only delete exact path match.
                If False, delete all objects with this path prefix.
        """
        response = await self.client.delete(self._get_object_route(path), params={"exact": exact})
        self._handle_response_status(response)

    async def get_presigned_download_url(
        self,
        source: dict[Literal["uid"], str],
        *,
        expire_in: Union[datetime.timedelta, int] = datetime.timedelta(hours=1),
    ) -> str:
        """Generate pre-signed download URL for an object.

        Args:
            source: Source object.
            expire_in: URL expiration time. Defaults to 1 hour.

        Returns:
            str: Pre-signed download URL.
        """
        response = await self.client.put(
            str(URL("/v1/presigned-urls/download/") / source["uid"]),
            data={
                "expire_at": self._get_expiration_date(expire_in).isoformat(),
            },
        )
        self._handle_response_status(response)

        return response.json()["presigned_download_url"]

    @asynccontextmanager
    async def read(self, obj: dict[Literal["uid"], str], *, stream=False):
        """Read the response content.

        Args:
            obj: Object to read.
            stream: If True, return a streaming response.

        Yields:
            httpx.Response: Response object.
        """
        download_url = (await self.get_by_uid(obj["uid"]))["download_url"]

        if stream:
            async with self.client.stream("GET", download_url) as response:
                self._handle_response_status(response)
                yield response
            return

        response = await self.client.get(download_url)
        self._handle_response_status(response)
        yield response
