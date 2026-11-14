import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from check_assets import PNG_SIGNATURE, png_dimensions


def chunk(kind, payload):
    checksum = zlib.crc32(kind + payload) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", checksum)


def png_bytes(raw=b"\x00\x20\x40\x60\xff", width=1, height=1,
              bit_depth=8, color_type=6, interlace=0, palette=None, compressed=None):
    ihdr = struct.pack(">IIBBBBB", width, height, bit_depth, color_type, 0, 0, interlace)
    if compressed is None:
        compressed = zlib.compress(raw)
    result = PNG_SIGNATURE + chunk(b"IHDR", ihdr)
    if palette is not None:
        result += chunk(b"PLTE", palette)
    return result + chunk(b"IDAT", compressed) + chunk(b"IEND", b"")


def valid_png():
    return png_bytes()


class PngValidationTests(unittest.TestCase):
    def check_bytes(self, data):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.png"
            path.write_bytes(data)
            return png_dimensions(path)

    def test_valid_png(self):
        self.assertEqual(self.check_bytes(valid_png()), (1, 1))

    def test_valid_adam7_png(self):
        self.assertEqual(self.check_bytes(png_bytes(interlace=1)), (1, 1))

    def test_accepts_split_consecutive_idat_chunks(self):
        ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0))
        compressed = zlib.compress(b"\x00\x20\x40\x60\xff")
        data = (PNG_SIGNATURE + ihdr + chunk(b"IDAT", compressed[:3])
                + chunk(b"IDAT", compressed[3:]) + chunk(b"IEND", b""))
        self.assertEqual(self.check_bytes(data), (1, 1))

    def test_valid_adam7_multi_pass_png(self):
        raw = (
            b"\x00\x10\x20\x30\xff"
            b"\x00\x40\x50\x60\xff"
            b"\x00\x70\x80\x90\xff\xa0\xb0\xc0\xff"
        )
        self.assertEqual(
            self.check_bytes(png_bytes(raw=raw, width=2, height=2, interlace=1)),
            (2, 2),
        )

    def test_valid_indexed_png_with_palette(self):
        self.assertEqual(
            self.check_bytes(
                png_bytes(
                    raw=b"\x00\x00",
                    bit_depth=1,
                    color_type=3,
                    palette=b"\x00\x00\x00\xff\xff\xff",
                )
            ),
            (1, 1),
        )

    def test_rejects_header_only_file(self):
        data = PNG_SIGNATURE + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0))
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

    def test_rejects_trailing_png_data(self):
        with self.assertRaisesRegex(ValueError, "data after IEND"):
            self.check_bytes(valid_png() + b"junk")

    def test_rejects_nonconsecutive_idat(self):
        ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0))
        image_data = zlib.compress(b"\x00\x20\x40\x60\xff")
        data = (PNG_SIGNATURE + ihdr + chunk(b"IDAT", image_data[:2])
                + chunk(b"tEXt", b"note\x00split")
                + chunk(b"IDAT", image_data[2:]) + chunk(b"IEND", b""))
        with self.assertRaisesRegex(ValueError, "IDAT chunks must be consecutive"):
            self.check_bytes(data)

    def test_rejects_duplicate_ihdr(self):
        ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0))
        with self.assertRaisesRegex(ValueError, "exactly one 13-byte IHDR"):
            self.check_bytes(PNG_SIGNATURE + ihdr + ihdr)

    def test_rejects_corrupt_zlib_checksum_even_with_valid_png_crc(self):
        compressed = bytearray(zlib.compress(b"\x00\x20\x40\x60\xff"))
        compressed[-1] ^= 0x01
        with self.assertRaisesRegex(ValueError, "zlib stream is invalid"):
            self.check_bytes(png_bytes(compressed=bytes(compressed)))

    def test_rejects_truncated_zlib_stream_even_with_valid_png_crc(self):
        compressed = zlib.compress(b"\x00\x20\x40\x60\xff")[:-2]
        with self.assertRaisesRegex(ValueError, "zlib stream is truncated"):
            self.check_bytes(png_bytes(compressed=compressed))

    def test_rejects_invalid_scanline_filter(self):
        with self.assertRaisesRegex(ValueError, "invalid filter type 5"):
            self.check_bytes(png_bytes(raw=b"\x05\x20\x40\x60\xff"))

    def test_rejects_wrong_decompressed_scanline_length(self):
        with self.assertRaisesRegex(ValueError, "expected 5"):
            self.check_bytes(png_bytes(raw=b"\x00\x20"))

    def test_rejects_trailing_bytes_after_zlib_stream(self):
        compressed = zlib.compress(b"\x00\x20\x40\x60\xff") + b"extra"
        with self.assertRaisesRegex(ValueError, "bytes after the zlib stream"):
            self.check_bytes(png_bytes(compressed=compressed))

    def test_rejects_indexed_png_without_palette(self):
        with self.assertRaisesRegex(ValueError, "missing its PLTE palette"):
            self.check_bytes(png_bytes(raw=b"\x00\x00", bit_depth=1, color_type=3))

    def test_rejects_palette_larger_than_index_bit_depth(self):
        palette = b"\x00\x00\x00" * 3
        with self.assertRaisesRegex(ValueError, "more entries than its bit depth"):
            self.check_bytes(png_bytes(raw=b"\x00\x00", bit_depth=1,
                                       color_type=3, palette=palette))


if __name__ == "__main__":
    unittest.main()
