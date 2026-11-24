#!/usr/bin/env python3
"""news-23 b100 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys
import zlib

SRC_NAME = "entry.png"
MIN_BYTES = 10_000
MAX_BYTES = 1_048_576


def fail(msg):
    print("ERROR:", msg, file=sys.stderr)
    return 1


def validate_png(data):
    """Check the PNG is a well-formed 1024x1024 image. Returns (width, height)."""
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("bad PNG signature")
    if len(data) > MAX_BYTES:
        raise ValueError("PNG larger than 1 MiB")
    if len(data) < MIN_BYTES:
        raise ValueError("PNG suspiciously small")
    pos = 8
    first = True
    width = height = None
    idat_total = 0
    idat_chunks = 0
    saw_iend = False
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + length > len(data):
            raise ValueError("truncated chunk %r" % ctype)
        chunk = data[pos + 8:pos + 8 + length]
        crc_stored = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])[0]
        crc_calc = zlib.crc32(ctype)
        crc_calc = zlib.crc32(chunk, crc_calc) & 0xFFFFFFFF
        if crc_calc != crc_stored:
            raise ValueError("bad CRC in chunk %r" % ctype)
        if first:
            if ctype != b"IHDR" or length != 13:
                raise ValueError("first chunk must be a 13-byte IHDR")
            width, height, depth, ctype2, comp, filt, inter = struct.unpack(">IIBBBBB", chunk)
            if (width, height) != (1024, 1024):
                raise ValueError("expected 1024x1024, got %dx%d" % (width, height))
            if depth != 8 or ctype2 not in (2, 6):
                raise ValueError("expected 8-bit RGB/RGBA, got depth %d type %d" % (depth, ctype2))
            if comp != 0 or filt != 0 or inter != 0:
                raise ValueError("unexpected compression/filter/interlace flags")
            first = False
        if ctype == b"IDAT":
            if length == 0:
                raise ValueError("empty IDAT chunk")
            idat_total += length
            idat_chunks += 1
        if ctype == b"IEND":
            if length != 0:
                raise ValueError("IEND must be empty")
            if pos + 12 + length != len(data):
                raise ValueError("trailing data after IEND")
            saw_iend = True
            break
        pos += 12 + length
    if first:
        raise ValueError("no IHDR found")
    if not saw_iend:
        raise ValueError("no IEND chunk")
    if idat_chunks == 0:
        raise ValueError("no IDAT chunk")
    if idat_total < 1000:
        raise ValueError("no usable image data (IDAT payload too small)")
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is not set")
    out_dir_abs = os.path.abspath(out_dir)
    if os.path.isfile(out_dir_abs):
        return fail("MAKEFUN_OUTPUT_DIR is a file, not a directory")
    # Never write inside the repo / next to main.py (resolve symlinks too).
    if os.path.commonpath([os.path.realpath(out_dir_abs), os.path.realpath(here)]) == os.path.realpath(here):
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the entry repo")
    if not os.path.isfile(src):
        return fail("entry.png not found next to main.py: %s" % src)
    with open(src, "rb") as f:
        data = f.read()
    try:
        w, h = validate_png(data)
    except ValueError as e:
        return fail("entry.png failed validation: %s" % e)
    out_path = os.path.join(out_dir_abs, SRC_NAME)
    if os.path.abspath(out_path) == os.path.abspath(src):
        return fail("output path would overwrite the source")
    os.makedirs(out_dir_abs, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(data)
    with open(out_path, "rb") as f:
        back = f.read()
    if back != data:
        return fail("output differs from source after write")
    print("wrote %s (%d bytes, %dx%d, sha256 %s)"
          % (out_path, len(data), w, h, hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
