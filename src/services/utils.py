import base64
import binascii


def base64_to_bytes_image(base64_image: str) -> bytes | None:
    try:
        return base64.b64decode(str.encode(base64_image))
    except binascii.Error:
        return None
