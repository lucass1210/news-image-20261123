"""Sum up 23 November 2026 world news in one image.

The entry image is bundled in this repository as image.png.b64
(base64 of the PNG, so the repository stays plain UTF-8 text).
This program deterministically decodes it to /output/entry.png,
with no network access, so two runs write identical bytes.
"""
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "image.png.b64")
DST_DIR = "/output"
DST = os.path.join(DST_DIR, "entry.png")


def main():
    os.makedirs(DST_DIR, exist_ok=True)
    with open(SRC, "r", encoding="utf-8") as f:
        data = base64.b64decode(f.read())
    with open(DST, "wb") as f:
        f.write(data)
    size = os.path.getsize(DST)
    assert size <= 1_048_576, f"entry.png is {size} bytes, over the 1 MiB cap"
    print(f"Wrote {DST} ({size} bytes)")


if __name__ == "__main__":
    main()
