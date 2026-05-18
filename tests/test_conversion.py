"""
Tests for audio_utils.mono_to_stereo — the core audio conversion function.

TDD: RED phase — write failing tests first.
"""

import struct
import pytest
from audio_utils import mono_to_stereo
from tests.conftest import s16_to_bytes, build_mono_pcm16, read_stereo_pcm16


# ─── RED: เสียก่อน → GREEN: ทำผ่าน → REFACTOR: จัดระเบียบ ───


class TestMonoToStereoBasic:
    """Basic sanity: edge cases, shape, identity."""

    def test_empty_input_returns_empty(self):
        """RED: empty mono → empty stereo."""
        result = mono_to_stereo(b"")
        assert result == b""

    def test_output_is_twice_input_length(self):
        """RED: stereo output must be exactly 2x mono input length."""
        mono = build_mono_pcm16([0, 100, -100, 32767])
        result = mono_to_stereo(mono, gain=1.0)
        assert len(result) == len(mono) * 2

    def test_gain_one_leaves_samples_unchanged(self):
        """RED: gain=1.0 → sample values must not change."""
        test_values = [0, 1, -1, 10000, -10000, 32767, -32768]
        for val in test_values:
            mono = build_mono_pcm16([val])
            result = mono_to_stereo(mono, gain=1.0)
            samples = read_stereo_pcm16(result)
            # L and R should both equal original value
            assert samples[0] == val, f"L channel mismatch for input {val}"
            assert samples[1] == val, f"R channel mismatch for input {val}"


class TestMonoToStereoGain:
    """Gain boost behaviour."""

    def test_gain_three_multiplies_samples(self):
        """RED: gain=3.0 → sample × 3."""
        mono = build_mono_pcm16([10000])
        result = mono_to_stereo(mono, gain=3.0)
        samples = read_stereo_pcm16(result)
        assert samples[0] == 30000
        assert samples[1] == 30000

    def test_gain_two_on_negative(self):
        """RED: negative sample with gain works correctly."""
        mono = build_mono_pcm16([-10000])
        result = mono_to_stereo(mono, gain=2.0)
        samples = read_stereo_pcm16(result)
        assert samples[0] == -20000

    def test_gain_zero_returns_silence(self):
        """RED: gain=0 → all samples zero."""
        mono = build_mono_pcm16([10000, 20000, -15000])
        result = mono_to_stereo(mono, gain=0.0)
        samples = read_stereo_pcm16(result)
        assert all(s == 0 for s in samples)


class TestMonoToStereoClamping:
    """Clipping prevention: must not overflow 16-bit signed range."""

    def test_clamp_positive_overflow(self):
        """RED: 20000 × 3.0 = 60000 → clamp to 32767."""
        mono = build_mono_pcm16([20000])
        result = mono_to_stereo(mono, gain=3.0)
        samples = read_stereo_pcm16(result)
        assert samples[0] == 32767

    def test_clamp_extreme_positive(self):
        """RED: 30000 × 2.0 = 60000 → clamp to 32767."""
        mono = build_mono_pcm16([30000])
        result = mono_to_stereo(mono, gain=2.0)
        samples = read_stereo_pcm16(result)
        assert samples[0] == 32767

    def test_clamp_negative_overflow(self):
        """RED: -20000 × 3.0 = -60000 → clamp to -32768."""
        mono = build_mono_pcm16([-20000])
        result = mono_to_stereo(mono, gain=3.0)
        samples = read_stereo_pcm16(result)
        assert samples[0] == -32768

    def test_max_value_no_clamp(self):
        """RED: 32767 × 1.0 stays at 32767 (boundary)."""
        mono = build_mono_pcm16([32767])
        result = mono_to_stereo(mono, gain=1.0)
        samples = read_stereo_pcm16(result)
        assert samples[0] == 32767

    def test_min_value_no_clamp(self):
        """RED: -32768 × 1.0 stays at -32768 (boundary)."""
        mono = build_mono_pcm16([-32768])
        result = mono_to_stereo(mono, gain=1.0)
        samples = read_stereo_pcm16(result)
        assert samples[0] == -32768


class TestMonoToStereoInterleaving:
    """Stereo interleaving: L and R must be identical per sample pair."""

    def test_multiple_samples_interleaved_correctly(self):
        """RED: 4 mono samples → 8 values, alternating L=R for each."""
        mono = build_mono_pcm16([100, 200, 300, 400])
        result = mono_to_stereo(mono, gain=1.0)
        samples = read_stereo_pcm16(result)

        assert len(samples) == 8  # 4 samples × 2 channels
        # Pair 0: sample 0
        assert samples[0] == 100  # L0
        assert samples[1] == 100  # R0
        # Pair 1: sample 1
        assert samples[2] == 200  # L1
        assert samples[3] == 200  # R1
        # Pair 2: sample 2
        assert samples[4] == 300  # L2
        assert samples[5] == 300  # R2
        # Pair 3: sample 3
        assert samples[6] == 400  # L3
        assert samples[7] == 400  # R3

    def test_byte_order_little_endian(self):
        """RED: verify byte encoding matches little-endian PCM16."""
        # 0xABCD in LE = [0xCD, 0xAB]
        # But signed. 0xABCD as signed = -21585
        # Let's use a clean value: 0x1234 = 4660
        mono = bytes([0x34, 0x12])  # one sample = 4660
        result = mono_to_stereo(mono, gain=1.0)
        # Expected: 4660 on L, 4660 on R
        # Each as LE: [0x34, 0x12]
        # Interleaved: [0x34, 0x12, 0x34, 0x12]
        assert result == bytes([0x34, 0x12, 0x34, 0x12])


class TestMonoToStereoRealValues:
    """Test with realistic values that the app actually uses."""

    def test_quiet_mic_simulation(self):
        """RED: realistic quiet mic sample with gain=3.0."""
        # Very quiet: sample = 500
        mono = build_mono_pcm16([500])
        result = mono_to_stereo(mono, gain=3.0)
        samples = read_stereo_pcm16(result)
        assert samples[0] == 1500  # 500 × 3

    def test_loud_but_safe(self):
        """RED: gain=3.0 on a moderately loud sample (no clip)."""
        # Sample = 10000, gain=3.0 = 30000 (safe under 32767)
        mono = build_mono_pcm16([10000])
        result = mono_to_stereo(mono, gain=3.0)
        samples = read_stereo_pcm16(result)
        assert samples[0] == 30000
        assert samples[1] == 30000


class TestMonoToStereoEdgeCases:
    """Edge cases and inputs that might break things."""

    def test_gain_too_high_still_safe(self):
        """RED: extreme gain 100x still doesn't overflow (clamps to max)."""
        mono = build_mono_pcm16([10000])
        result = mono_to_stereo(mono, gain=100.0)
        samples = read_stereo_pcm16(result)
        assert samples[0] == 32767  # clamped

    def test_odd_length_input(self):
        """RED: input with odd number of bytes → last byte ignored?"""
        # Actually PCM16 must be even length. Let's see what happens.
        # This is a realistic edge case — server might get partial data.
        mono = b'\x10\x27\x00'  # 3 bytes = 1.5 samples
        result = mono_to_stereo(mono, gain=1.0)
        # Should still process first complete sample
        assert len(result) == 4  # processed 2 bytes out of 3
        samples = read_stereo_pcm16(result)
        assert len(samples) == 2
        assert samples[0] == 10000  # 0x2710 = 10000
        assert samples[1] == 10000

    def test_all_zeros_input(self):
        """RED: silence in → silence out."""
        mono = bytes(1024)  # 512 samples of silence
        result = mono_to_stereo(mono, gain=3.0)
        assert len(result) == 2048
        assert all(b == 0 for b in result)
