#!/usr/bin/env python3
"""Comprehensive tests for timing utilities."""
# this_file: tests/test_timing.py

from datetime import timedelta

import pytest

from camtasio.utils.timing import FrameStamp


class TestFrameStamp:
    """Test FrameStamp class for frame-based timing."""

    def test_framestamp_creation(self):
        """Test basic FrameStamp creation."""
        fs = FrameStamp(100, 30)
        assert fs.frame_number == 100
        assert fs.frame_rate == 30

    def test_framestamp_validation(self):
        """Test FrameStamp parameter validation."""
        # Test negative frame rate
        with pytest.raises(ValueError, match="Frame rate must be positive"):
            FrameStamp(100, 0)

        with pytest.raises(ValueError, match="Frame rate must be positive"):
            FrameStamp(100, -30)

        # Test negative frame number
        with pytest.raises(ValueError, match="Frame number must be non-negative"):
            FrameStamp(-1, 30)

    def test_framestamp_time_property(self):
        """Test FrameStamp time property."""
        fs = FrameStamp(150, 30)  # 5 seconds
        assert fs.time == timedelta(seconds=5.0)

        fs = FrameStamp(75, 30)  # 2.5 seconds
        assert fs.time == timedelta(seconds=2.5)

        fs = FrameStamp(1, 30)  # 1/30 second
        expected = timedelta(seconds=1 / 30)
        assert abs(fs.time.total_seconds() - expected.total_seconds()) < 1e-10

    def test_framestamp_total_seconds(self):
        """Test FrameStamp total_seconds property."""
        fs = FrameStamp(150, 30)
        assert fs.total_seconds == 5.0

        fs = FrameStamp(75, 30)
        assert fs.total_seconds == 2.5

        fs = FrameStamp(1, 30)
        assert abs(fs.total_seconds - (1 / 30)) < 1e-10

    def test_framestamp_frame_time(self):
        """Test FrameStamp frame_time property."""
        # Exact seconds
        fs = FrameStamp(150, 30)  # 5 seconds, 0 frames
        seconds, frames = fs.frame_time
        assert seconds == timedelta(seconds=5)
        assert frames == 0

        # Partial seconds
        fs = FrameStamp(155, 30)  # 5 seconds, 5 frames
        seconds, frames = fs.frame_time
        assert seconds == timedelta(seconds=5)
        assert frames == 5

        # Less than one second
        fs = FrameStamp(15, 30)  # 0 seconds, 15 frames
        seconds, frames = fs.frame_time
        assert seconds == timedelta(seconds=0)
        assert frames == 15

    def test_framestamp_from_seconds(self):
        """Test creating FrameStamp from seconds."""
        fs = FrameStamp.from_seconds(5.0, 30)
        assert fs.frame_number == 150
        assert fs.frame_rate == 30

        fs = FrameStamp.from_seconds(2.5, 30)
        assert fs.frame_number == 75
        assert fs.frame_rate == 30

        # Test rounding
        fs = FrameStamp.from_seconds(1 / 30 + 0.001, 30)  # Slightly more than 1 frame
        assert fs.frame_number == 1  # Should round to nearest frame

    def test_framestamp_from_timedelta(self):
        """Test creating FrameStamp from timedelta."""
        td = timedelta(seconds=5)
        fs = FrameStamp.from_timedelta(td, 30)
        assert fs.frame_number == 150
        assert fs.frame_rate == 30

        td = timedelta(seconds=2, milliseconds=500)
        fs = FrameStamp.from_timedelta(td, 30)
        assert fs.frame_number == 75
        assert fs.frame_rate == 30

    def test_framestamp_string_representation(self):
        """Test FrameStamp string representations."""
        fs = FrameStamp(155, 30)  # 5 seconds, 5 frames
        assert str(fs) == "5;5"

        fs = FrameStamp(150, 30)  # 5 seconds, 0 frames
        assert str(fs) == "5;0"

        fs = FrameStamp(15, 30)  # 0 seconds, 15 frames
        assert str(fs) == "0;15"

        # Test repr
        fs = FrameStamp(100, 30)
        assert repr(fs) == "FrameStamp(frame_number=100, frame_rate=30)"

    def test_framestamp_comparison(self):
        """Test FrameStamp comparison operations."""
        fs1 = FrameStamp(100, 30)  # 100/30 seconds
        fs2 = FrameStamp(150, 30)  # 150/30 seconds
        fs3 = FrameStamp(200, 60)  # 200/60 = 100/30 seconds (same as fs1)

        # Less than
        assert fs1 < fs2
        assert not fs2 < fs1
        assert not fs1 < fs3  # Equal times

        # Less than or equal
        assert fs1 <= fs2
        assert fs1 <= fs3  # Equal times
        assert not fs2 <= fs1

        # Greater than
        assert fs2 > fs1
        assert not fs1 > fs2
        assert not fs1 > fs3  # Equal times

        # Greater than or equal
        assert fs2 >= fs1
        assert fs1 >= fs3  # Equal times
        assert not fs1 >= fs2

    def test_framestamp_addition(self):
        """Test FrameStamp addition."""
        fs1 = FrameStamp(100, 30)  # 100/30 seconds
        fs2 = FrameStamp(50, 30)  # 50/30 seconds

        result = fs1 + fs2
        assert result.frame_number == 150  # 100 + 50
        assert result.frame_rate == 30

        # Test addition with different frame rates
        fs3 = FrameStamp(100, 60)  # 100/60 seconds
        result = fs1 + fs3
        # Should use LCM of frame rates (60)
        assert result.frame_rate == 60
        # fs1: 100/30 = 200/60, fs3: 100/60, sum: 300/60
        assert result.frame_number == 300

    def test_framestamp_subtraction(self):
        """Test FrameStamp subtraction."""
        fs1 = FrameStamp(150, 30)  # 150/30 seconds
        fs2 = FrameStamp(50, 30)  # 50/30 seconds

        result = fs1 - fs2
        assert result.frame_number == 100  # 150 - 50
        assert result.frame_rate == 30

        # Test subtraction with different frame rates
        fs3 = FrameStamp(50, 60)  # 50/60 seconds
        result = fs1 - fs3
        # Should use LCM of frame rates (60)
        assert result.frame_rate == 60
        # fs1: 150/30 = 300/60, fs3: 50/60, diff: 250/60
        assert result.frame_number == 250

    def test_framestamp_lcm_calculation(self):
        """Test LCM calculation in frame rate conversion."""
        fs1 = FrameStamp(120, 24)  # 24 fps
        fs2 = FrameStamp(150, 30)  # 30 fps

        # LCM of 24 and 30 is 120
        result = fs1 + fs2
        assert result.frame_rate == 120

        # fs1: 120/24 = 600/120 (5 seconds)
        # fs2: 150/30 = 600/120 (5 seconds)
        # sum: 1200/120 (10 seconds)
        assert result.frame_number == 1200

    def test_framestamp_to_frame_rate(self):
        """Test converting FrameStamp to different frame rate."""
        fs = FrameStamp(150, 30)  # 5 seconds at 30fps

        # Convert to 60fps
        fs_60 = fs.to_frame_rate(60)
        assert fs_60.frame_rate == 60
        assert fs_60.frame_number == 300  # 5 seconds * 60fps
        assert fs_60.total_seconds == fs.total_seconds  # Same duration

        # Convert to 24fps
        fs_24 = fs.to_frame_rate(24)
        assert fs_24.frame_rate == 24
        assert fs_24.frame_number == 120  # 5 seconds * 24fps
        assert (
            abs(fs_24.total_seconds - fs.total_seconds) < 1e-10
        )  # Same duration (within rounding)

    def test_framestamp_zero_values(self):
        """Test FrameStamp with zero frame number."""
        fs = FrameStamp(0, 30)
        assert fs.frame_number == 0
        assert fs.frame_rate == 30
        assert fs.total_seconds == 0.0
        assert fs.time == timedelta(0)

        seconds, frames = fs.frame_time
        assert seconds == timedelta(0)
        assert frames == 0

        assert str(fs) == "0;0"

    def test_framestamp_high_precision(self):
        """Test FrameStamp with high precision frame rates."""
        # Test with high frame rate
        fs = FrameStamp(1000, 1000)  # 1 second at 1000fps
        assert fs.total_seconds == 1.0

        # Test with fractional seconds
        fs = FrameStamp(1, 1000)  # 1/1000 second
        assert abs(fs.total_seconds - 0.001) < 1e-10


class TestFrameStampArithmetic:
    """Test FrameStamp arithmetic operations."""

    def test_addition_same_frame_rate(self):
        """Test addition with same frame rate."""
        fs1 = FrameStamp(100, 30)
        fs2 = FrameStamp(200, 30)

        result = fs1 + fs2
        assert result.frame_number == 300
        assert result.frame_rate == 30

    def test_addition_different_frame_rates(self):
        """Test addition with different frame rates."""
        fs1 = FrameStamp(60, 30)  # 2 seconds
        fs2 = FrameStamp(120, 60)  # 2 seconds

        result = fs1 + fs2
        # LCM of 30 and 60 is 60
        assert result.frame_rate == 60
        # fs1: 60/30 = 120/60, fs2: 120/60, sum: 240/60 (4 seconds)
        assert result.frame_number == 240
        assert result.total_seconds == 4.0

    def test_subtraction_same_frame_rate(self):
        """Test subtraction with same frame rate."""
        fs1 = FrameStamp(300, 30)
        fs2 = FrameStamp(100, 30)

        result = fs1 - fs2
        assert result.frame_number == 200
        assert result.frame_rate == 30

    def test_subtraction_different_frame_rates(self):
        """Test subtraction with different frame rates."""
        fs1 = FrameStamp(180, 30)  # 6 seconds
        fs2 = FrameStamp(120, 60)  # 2 seconds

        result = fs1 - fs2
        # LCM of 30 and 60 is 60
        assert result.frame_rate == 60
        # fs1: 180/30 = 360/60, fs2: 120/60, diff: 240/60 (4 seconds)
        assert result.frame_number == 240
        assert result.total_seconds == 4.0

    def test_arithmetic_with_zero(self):
        """Test arithmetic operations with zero values."""
        fs = FrameStamp(100, 30)
        zero = FrameStamp(0, 30)

        # Addition with zero
        result = fs + zero
        assert result.frame_number == 100
        assert result.frame_rate == 30

        # Subtraction with zero
        result = fs - zero
        assert result.frame_number == 100
        assert result.frame_rate == 30

        # Zero minus something should raise ValueError (negative not allowed)
        with pytest.raises(ValueError, match="Frame number must be non-negative"):
            result = zero - fs


class TestFrameStampEdgeCases:
    """Test FrameStamp edge cases and boundary conditions."""

    def test_very_high_frame_rates(self):
        """Test with very high frame rates."""
        fs = FrameStamp(10000, 10000)  # 1 second
        assert fs.total_seconds == 1.0

        fs = FrameStamp(1, 10000)  # 0.0001 seconds
        assert abs(fs.total_seconds - 0.0001) < 1e-10

    def test_very_low_frame_rates(self):
        """Test with very low frame rates."""
        fs = FrameStamp(1, 1)  # 1 second
        assert fs.total_seconds == 1.0

        fs = FrameStamp(2, 1)  # 2 seconds
        assert fs.total_seconds == 2.0

    def test_large_frame_numbers(self):
        """Test with large frame numbers."""
        # 1 hour at 30fps = 108,000 frames
        fs = FrameStamp(108000, 30)
        assert fs.total_seconds == 3600.0  # 1 hour

        # 24 hours at 30fps = 2,592,000 frames
        fs = FrameStamp(2592000, 30)
        assert fs.total_seconds == 86400.0  # 24 hours

    def test_frame_rate_conversion_precision(self):
        """Test precision in frame rate conversions."""
        # Create a timestamp that doesn't divide evenly
        fs = FrameStamp(100, 30)  # 100/30 = 3.333... seconds

        # Convert to 24fps
        fs_24 = fs.to_frame_rate(24)
        # 3.333... * 24 = 80 frames (rounded)
        assert fs_24.frame_number == 80

        # Convert back to 30fps
        fs_30_back = fs_24.to_frame_rate(30)
        # 80/24 * 30 = 100 frames (should be exact due to rounding)
        assert fs_30_back.frame_number == 100

    def test_common_frame_rate_conversions(self):
        """Test conversions between common frame rates."""
        # 24fps to 30fps
        fs_24 = FrameStamp(240, 24)  # 10 seconds
        fs_30 = fs_24.to_frame_rate(30)
        assert fs_30.frame_number == 300  # 10 seconds at 30fps

        # 30fps to 60fps
        fs_30 = FrameStamp(300, 30)  # 10 seconds
        fs_60 = fs_30.to_frame_rate(60)
        assert fs_60.frame_number == 600  # 10 seconds at 60fps

        # 60fps to 24fps
        fs_60 = FrameStamp(600, 60)  # 10 seconds
        fs_24 = fs_60.to_frame_rate(24)
        assert fs_24.frame_number == 240  # 10 seconds at 24fps


class TestFrameStampInvalidOperations:
    """Test FrameStamp invalid operations and error handling."""

    def test_comparison_with_non_framestamp(self):
        """Test comparison with non-FrameStamp objects."""
        fs = FrameStamp(100, 30)

        # Comparisons with non-FrameStamp objects should raise TypeError
        with pytest.raises(TypeError):
            _ = fs < "not a framestamp"
        with pytest.raises(TypeError):
            _ = fs <= 123
        with pytest.raises(TypeError):
            _ = fs > 45.6
        with pytest.raises(TypeError):
            _ = fs >= None

    def test_arithmetic_with_non_framestamp(self):
        """Test arithmetic with non-FrameStamp objects."""
        fs = FrameStamp(100, 30)

        # Arithmetic with non-FrameStamp objects should raise TypeError
        with pytest.raises(TypeError):
            fs + "not a framestamp"
        with pytest.raises(TypeError):
            fs - 123

    def test_negative_result_from_subtraction(self):
        """Test that subtraction resulting in negative frame numbers raises error."""
        fs1 = FrameStamp(50, 30)
        fs2 = FrameStamp(100, 30)

        # Subtracting larger from smaller should raise ValueError
        with pytest.raises(ValueError, match="Frame number must be non-negative"):
            fs1 - fs2
