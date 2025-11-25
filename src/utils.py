import io
from PIL import Image


def pil_to_bytes(image: Image.Image, format: str = "PNG") -> bytes:
    buf = io.BytesIO()
    image.save(buf, format=format)
    buf.seek(0)
    return buf.getvalue()
