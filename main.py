"""Sum up 23 November 2026 world news in one image.

The entry image is bundled in this repository as image.png.b64
(base64 of the PNG, so the repository stays plain UTF-8 text).
This program deterministically decodes it to /output/entry.png,
with no network access, so two runs write identical bytes.
Before writing, it validates the result: the bytes must be a real
PNG and the picture must be 1024x1024, the size this entry promises.
"""
import base64
import binascii
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "image.png.b64")
DST_DIR = "/output"
DST = os.path.join(DST_DIR, "entry.png")

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def read_png_dimensions(data):
    """Return (width, height) from a PNG's IHDR chunk, stdlib only."""
    if len(data) < 24 or data[:8] != PNG_MAGIC:
        raise ValueError("decoded bytes are not a PNG file")
    if data[12:16] != b"IHDR":
        raise ValueError("PNG has no IHDR chunk where one is expected")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main():
    os.makedirs(DST_DIR, exist_ok=True)
    try:
        with open(SRC, "r", encoding="utf-8") as f:
            text = "".join(f.read().split())
        data = base64.b64decode(text, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise SystemExit(f"image.png.b64 is not valid base64: {exc}")
    width, height = read_png_dimensions(data)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise SystemExit(
            f"entry.png is {width}x{height}, expected "
            f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )
    with open(DST, "wb") as f:
        f.write(data)
    size = os.path.getsize(DST)
    assert size <= 1_048_576, f"entry.png is {size} bytes, over the 1 MiB cap"
    print(f"Wrote {DST} ({size} bytes, {width}x{height})")


if __name__ == "__main__":
    main()
