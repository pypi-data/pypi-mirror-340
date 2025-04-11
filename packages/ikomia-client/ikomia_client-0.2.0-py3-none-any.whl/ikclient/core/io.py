"""Deployment Input/Output classes."""

from abc import ABC
from pathlib import Path
from typing import Generic, Literal, TypedDict, TypeVar, Union

import numpy as np
from PIL.Image import Image
from typing_extensions import NotRequired

import ikclient.utils.image
from ikclient.storage.client import StorageObject

K = TypeVar("K")
D = TypeVar("D")


class BaseTaskIO(ABC, Generic[K, D]):
    """Base class for task input/output."""

    def __init__(self, raw_or_self: Union[dict[K, D], "BaseTaskIO[K, D]"]):
        """Initialize a new task input/output.

        Args:
            raw_or_self: Raw task input/output data or another BaseTaskIO instance
        """
        self.raw: dict[K, D]

        if isinstance(raw_or_self, BaseTaskIO):
            self.raw = raw_or_self.raw
        else:
            self.raw = raw_or_self

    @property
    def key(self) -> K:
        """Get type of task input/output.

        Returns:
            Type of task input/output
        """
        return next(iter(self.raw.keys()))

    @property
    def data(self) -> D:
        """Get data of task input/output.

        Returns:
            Data of task input/output
        """
        return next(iter(self.raw.values()))

    def __getitem__(self, key):
        """Shortcut to TaskIO.data[key] for dict-like access.

        Args:
            key: key to access in data

        Returns:
            Value associated with the key in data
        """
        return self.data[key]

    def get(self, key, default=None):
        """Shortcut to TaskIO.data.get(key) for dict-like access.

        Args:
            key: key to access in data
            default: default value if key not found. Defaults to None.

        Returns:
            Value associated with the key in data or default value
        """
        try:
            return self.data[key]
        except KeyError:
            return default

    def __repr__(self) -> str:
        """Get string representation of task input/output.

        Returns:
            String representation
        """
        data_rep = self.data.__repr__()
        if isinstance(data_rep, str) and len(data_rep) > 500:
            data_rep = data_rep[:500] + "..."

        return f"{self.__class__.__name__}({{{self.key}: {data_rep}}})"


class TaskIO(BaseTaskIO[str, Union[str, dict]]):
    """Class for task input/output."""


class ImageIO(BaseTaskIO[Literal["image"], str]):
    """Class for image input/output."""

    @classmethod
    def create(cls, inp: Union[str, Path, bytes, Image]) -> "ImageIO":
        """Create an ImageIO instance from an image.

        Args:
            inp: PIL Image, bytes, or path to image file

        Returns:
            ImageIO instance
        """
        if isinstance(inp, bytes):
            b64_str = ikclient.utils.image.image_bytes_to_b64_str(inp)
            return cls({"image": b64_str})
        if isinstance(inp, Image):
            b64_str = ikclient.utils.image.pil_image_to_b64_str(inp)
            return cls({"image": b64_str})

        with open(inp, "rb") as f:
            b64_str = ikclient.utils.image.image_bytes_to_b64_str(f.read())
            return cls({"image": b64_str})

    @property
    def format(self) -> str:
        """Get image format."""
        pil_format = self.to_pil().format
        return pil_format.lower() if pil_format else ""

    def to_pil(self) -> Image:
        """Convert image data to PIL Image.

        Returns:
            PIL Image
        """
        return ikclient.utils.image.b64_str_to_pil_image(self.data)

    def to_numpy(self):
        """Convert image data to numpy array.

        Returns:
            Image as numpy array
        """
        return np.array(self.to_pil())

    def to_bytes(self) -> bytes:
        """Convert image data to bytes.

        Returns:
            Image as bytes
        """
        return ikclient.utils.image.b64_str_to_image_bytes(self.data)


class _StorageObjectIO(TypedDict):
    url: str
    data_type: str
    metadata: NotRequired[StorageObject]


class StorageObjectIO(BaseTaskIO[Literal["storage_object"], _StorageObjectIO]):
    """Class for storage object input/output."""
