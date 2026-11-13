import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from check_assets import PNG_SIGNATURE, png_dimensions


def chunk(kind, payload):
    checksum = zlib.crc32(kind + payload) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", checksum)


def valid_png():
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)
    pixels = zlib.compress(b"\x00\x20\x40\x60\xff")
    return (
        PNG_SIGNATURE
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", pixels)
        + chunk(b"IEND", b"")
    )


class PngValidationTests(unittest.TestCase):
    def check_bytes(self, data):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.png"
            path.write_bytes(data)
            return png_dimensions(path)

    def test_valid_png(self):
        self.assertEqual(self.check_bytes(valid_png()), (1, 1))

    def test_rejects_header_only_file(self):
        data = PNG_SIGNATURE + chunk(
            b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)
        )
        with self.assertRaisesRegex(ValueError, "truncated PNG chunk header"):
            self.check_bytes(data)

    def test_rejects_bad_chunk_crc(self):
        data = bytearray(valid_png())
        data[-1] ^= 0x01
        with self.assertRaisesRegex(ValueError, "CRC mismatch"):
            self.check_bytes(bytes(data))

    def test_rejects_missing_iend(self):
        data = valid_png()
        iend = chunk(b"IEND", b"")
        with self.assertRaisesRegex(ValueError, "truncated PNG chunk header"):
            self.check_bytes(data[:-len(iend)])

    def test_rejects_trailing_data(self):
        with self.assertRaisesRegex(ValueError, "data after IEND"):
            self.check_bytes(valid_png() + b"junk")

    def test_rejects_nonconsecutive_idat(self):
        ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0))
        image_data = zlib.compress(b"\x00\x20\x40\x60\xff")
        data = (
            PNG_SIGNATURE + ihdr + chunk(b"IDAT", image_data[:2])
            + chunk(b"tEXt", b"note\x00split")
            + chunk(b"IDAT", image_data[2:]) + chunk(b"IEND", b"")
        )
        with self.assertRaisesRegex(ValueError, "IDAT chunks must be consecutive"):
            self.check_bytes(data)

    def test_rejects_duplicate_ihdr(self):
        ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0))
        data = PNG_SIGNATURE + ihdr + ihdr
        with self.assertRaisesRegex(ValueError, "exactly one 13-byte IHDR"):
            self.check_bytes(data)


if __name__ == "__main__":
    unittest.main()
