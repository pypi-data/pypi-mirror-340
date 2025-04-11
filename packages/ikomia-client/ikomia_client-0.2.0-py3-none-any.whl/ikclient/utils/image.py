"""Transform image from / to base64."""

import base64
from io import BytesIO
from typing import Optional

from PIL import Image


def pil_image_to_b64_str(image: Image.Image, image_format: Optional[str] = None) -> str:
    """Convert PIL.Image.Image data to base 64 string.

    Args:
        image: source image to convert
        image_format: set image format (compression) before converting to b64. None mean keep same format.

    Returns:
        Base 64 string of image
    """
    if image_format is None:
        image_format = "JPEG" if image.format is None else image.format

    buffered = BytesIO()
    image.save(buffered, format=image_format)
    image_bytes = base64.b64encode(buffered.getvalue())
    image_str = image_bytes.decode("UTF-8")
    return image_str


def image_bytes_to_b64_str(b: bytes) -> str:
    """Convert bytes to base 64 string.

    Args:
        b: bytes of image

    Returns:
        Base 64 string of image
    """
    b64_image = base64.b64encode(b)
    return b64_image.decode("UTF-8")


def b64_str_to_pil_image(b64_image: str) -> Image.Image:
    """Convert b64 string of image to PIL image structure.

    Args:
        b64_image: base 64 string of image to convert

    Returns:
        Image as PIL.Image.Image structure
    """
    b64_bytes = b64_image.encode("UTF-8")
    b64_decoded_bytes = base64.b64decode(b64_bytes)
    bytes_obj = BytesIO(b64_decoded_bytes)
    img = Image.open(bytes_obj)
    return img


def b64_str_to_image_bytes(b64_image: str) -> bytes:
    """Convert base 64 string to bytes.

    Args:
        b64_image: base 64 string of image to convert

    Returns:
        Image as bytes
    """
    b64_bytes = b64_image.encode("UTF-8")
    return base64.b64decode(b64_bytes)
