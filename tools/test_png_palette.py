import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from check_assets import PNG_SIGNATURE, png_dimensions


def chunk(kind, payload):
    crc = zlib.crc32(kind + payload) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", crc)


def indexed_png(width, height, bit_depth, palette, scanlines):
    ihdr = struct.pack(">IIBBBBB", width, height, bit_depth, 3, 0, 0, 0)
    raw = b"".join(bytes([filter_type]) + encoded for filter_type, encoded in scanlines)
    return (
        PNG_SIGNATURE
        + chunk(b"IHDR", ihdr)
        + chunk(b"PLTE", palette)
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )


class PaletteIndexValidationTests(unittest.TestCase):
    def check_bytes(self, data):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.png"
            path.write_bytes(data)
            return png_dimensions(path)

    def test_reconstructs_all_png_filters_for_indexed_rows(self):
        palette = b"\x00\x00\x00\xff\xff\xff"
        # Row 1 decodes to [1, 0] against row 0 [0, 1].
        encoded_by_filter = {
            0: bytes([1, 0]),
            1: bytes([1, 255]),
            2: bytes([1, 255]),
            3: bytes([1, 255]),
            4: bytes([1, 255]),
        }
        for filter_type, encoded in encoded_by_filter.items():
            with self.subTest(filter_type=filter_type):
                data = indexed_png(
                    2, 2, 8, palette,
                    [(0, bytes([0, 1])), (filter_type, encoded)],
                )
                self.assertEqual(self.check_bytes(data), (2, 2))

    def test_rejects_out_of_range_index_after_up_filter(self):
        palette = b"\x00\x00\x00\xff\xff\xff"
        # Decodes to [2, 0] from previous row [0, 1]; index 2 is invalid.
        data = indexed_png(2, 2, 8, palette, [(0, bytes([0, 1])), (2, bytes([2, 255]))])
        with self.assertRaisesRegex(ValueError, "palette index 2"):
            self.check_bytes(data)

    def test_rejects_out_of_range_packed_indices(self):
        cases = [
            (1, 1, bytes([0x80]), 1),   # one-bit: index 1, only index 0 exists
            (2, 3, bytes([0xC0]), 1),   # two-bit: index 3, only indices 0..2 exist
            (4, 2, bytes([0xF0]), 1),   # four-bit: index 15, only indices 0..1 exist
            (8, 2, bytes([2]), 1),      # eight-bit: index 2, only indices 0..1 exist
        ]
        for bit_depth, palette_entries, pixels, width in cases:
            with self.subTest(bit_depth=bit_depth):
                palette = b"\x00\x00\x00" * palette_entries
                data = indexed_png(width, 1, bit_depth, palette, [(0, pixels)])
                with self.assertRaisesRegex(ValueError, "palette index"):
                    self.check_bytes(data)

    def test_accepts_packed_indexed_pixels_with_valid_palette(self):
        data = indexed_png(2, 1, 1, b"\x00\x00\x00\xff\xff\xff", [(0, bytes([0x80]))])
        self.assertEqual(self.check_bytes(data), (2, 1))


if __name__ == "__main__":
    unittest.main()
