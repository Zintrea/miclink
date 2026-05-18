"""
audio_utils.py — Pure audio utility functions for miclink

Contains functions that do NOT depend on PyAudio or any hardware.
These can be tested in any environment (including WSL without Windows audio).
"""


def mono_to_stereo(mono_bytes: bytes, gain: float = 3.0) -> bytes:
    """Convert mono PCM16 bytes to interleaved stereo PCM16 with gain boost.

    VB-Cable (device 27) produces garbled audio with mono output
    at 48000 Hz. Sending native stereo (L/R duplicate) fixes it.

    Args:
        mono_bytes: Raw PCM16 mono audio data (little-endian 16-bit signed)
        gain: Volume multiplier (default 3.0, range 1.0-5.0)

    Returns:
        PCM16 stereo audio data (2x length of input)
    """
    if not mono_bytes:
        return b""

    # Truncate to even length to handle partial WebSocket frames
    if len(mono_bytes) % 2 != 0:
        mono_bytes = mono_bytes[:-1]

    result = bytearray(len(mono_bytes) * 2)

    for i in range(0, len(mono_bytes), 2):
        # Read 16-bit signed little-endian sample
        sample = mono_bytes[i] | (mono_bytes[i + 1] << 8)

        # Convert from unsigned to signed (Python treats bytes as 0-255)
        if sample >= 32768:
            sample -= 65536

        # Apply gain boost
        sample = _clamp(int(sample * gain), -32768, 32767)

        # Convert back to unsigned for byte packing
        if sample < 0:
            sample += 65536

        # Write L and R channels with the same sample
        offset = i * 2
        result[offset] = sample & 0xFF
        result[offset + 1] = (sample >> 8) & 0xFF
        result[offset + 2] = sample & 0xFF
        result[offset + 3] = (sample >> 8) & 0xFF

    return bytes(result)


def _clamp(value: int, low: int, high: int) -> int:
    """Clamp value to [low, high] range."""
    if value > high:
        return high
    if value < low:
        return low
    return value
