"""Ultra-optimized JSD (JSON Database) file format implementation."""

import os
import struct
from pathlib import Path
from typing import Any, Dict, Optional, Union

import lz4.frame  # type: ignore
import msgspec


class JSD:
    """Ultra-optimized JSD file format handler."""

    # File format constants
    MAGIC_BYTES = b"JSD4"  # Updated format identifier
    HEADER_SIZE = 16  # Fixed size header

    # Compression options
    COMPRESSION_NONE = 0
    COMPRESSION_LZ4 = 1

    # Buffer size optimization - adaptive based on file size
    DEFAULT_BUFFER_SIZE = 256 * 1024  # 256KB default buffer (reduced from 1MB)

    def __init__(self, path: Union[str, Path]):
        """Initialize JSD file."""
        self.path = Path(path)
        self._data: Optional[Dict[str, Any]] = None

    def dumps(self, data: Dict[str, Any]) -> None:
        """Write data to JSD file with maximum performance."""
        # Cache the data
        self._data = data

        # Direct binary serialization with msgspec
        # Use the more efficient msgpack format instead of JSON
        packed_data = msgspec.msgpack.encode(data)

        # Compress with LZ4 frame format - better balance of speed and compression
        compressed_data = self._compress(packed_data)

        # Create header
        header = self._create_header(packed_data)

        # Write to file - optimized for speed
        self._write_file(header, compressed_data)

    def _write_file(self, header, compressed_data):
        # Use memoryview to avoid extra memory copies
        view = memoryview(compressed_data)

        # Optimize buffer size for better memory efficiency
        buffer_size = min(self.DEFAULT_BUFFER_SIZE, len(compressed_data) + len(header))

        with open(self.path, "wb", buffering=buffer_size) as f:
            f.write(header)
            f.write(view)

    def _create_header(self, packed_data) -> bytes:
        return (
            self.MAGIC_BYTES
            + bytes([self.COMPRESSION_LZ4])
            + bytes(3)  # Reserved bytes
            + struct.pack("<Q", len(packed_data))  # Original size
        )

    @staticmethod
    def _compress(data: bytes) -> bytes:
        # Use memoryview to avoid copies
        view = memoryview(data)

        # Using DEFAULT instead of MAX64KB saves memory without sacrificing speed
        return lz4.frame.compress(
            view,
            compression_level=1,  # Low compression for speed
            block_size=lz4.frame.BLOCKSIZE_DEFAULT,  # Better memory balance
            content_checksum=False,  # Skip checksum for speed
            block_linked=False,  # Skip block checksums for speed
            store_size=True,  # Store size for faster decompression
        )

    def loads(self) -> Dict[str, Any]:
        """Read data from JSD file with maximum performance."""
        # Return cached data if available
        if self._data is not None:
            return self._data

        try:
            # Calculate optimal buffer size based on file size
            buffer_size = self._calculate_bufffersize()

            # Read the entire file in one operation
            compressed_data = self._read(self.path, buffer_size)

            # Decompress data - using memoryview for efficiency
            binary_data = self._decompress(compressed_data)

            # Deserialize using msgpack (faster than JSON)
            self._data = self._deserialize(binary_data)
            return self._data

        except FileNotFoundError:
            self._data = {}
            return self._data
        except Exception as e:
            print(f"Error reading file: {e}")
            self._data = {}
            return self._data

    def _calculate_bufffersize(self) -> int:
        file_size = os.path.getsize(self.path)
        return min(self.DEFAULT_BUFFER_SIZE, file_size)

    def _read(self, path: Path, buffer_size: int) -> bytes:
        with open(self.path, "rb", buffering=buffer_size) as f:
            header = f.read(self.HEADER_SIZE)

            # Validate magic bytes
            if not self._is_valid_magic_bytes(header):
                raise ValueError(f"Not a valid JSD4 file: {self.path}")

            # Get compressed data
            compressed_data = f.read()
        return compressed_data

    @staticmethod
    def _decompress(compressed_data) -> bytes:
        return lz4.frame.decompress(memoryview(compressed_data))

    @staticmethod
    def _deserialize(binary_data):
        return msgspec.msgpack.decode(binary_data)

    def _is_valid_magic_bytes(self, header: bytes) -> bool:
        return header[: len(self.MAGIC_BYTES)] == self.MAGIC_BYTES
