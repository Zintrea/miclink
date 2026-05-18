"""Shared fixtures and helpers for miclink tests."""

import struct
from typing import List


def s16_to_bytes(value: int) -> bytes:
    """Convert a signed 16-bit integer to little-endian bytes."""
    return struct.pack('<h', value)


def build_mono_pcm16(samples: List[int]) -> bytes:
    """Build mono PCM16 bytes from a list of signed 16-bit sample values."""
    return b''.join(s16_to_bytes(s) for s in samples)


def read_stereo_pcm16(data: bytes) -> List[int]:
    """Read stereo PCM16 bytes into a list of signed 16-bit interleaved samples.

    Returns [L1, R1, L2, R2, ...]
    """
    assert len(data) % 4 == 0, f"Stereo data must be multiple of 4 bytes, got {len(data)}"
    return list(struct.unpack(f'<{len(data)//2}h', data))
