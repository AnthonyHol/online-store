import base64


def base64_to_bytes_image(base64_image: str) -> bytes | None:
    try:
        return base64.b64decode(base64_image.encode())
    except:
        return None
