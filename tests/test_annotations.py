#!/usr/bin/env python3
"""Comprehensive tests for the annotations system."""
# this_file: tests/test_annotations.py

import pytest

from camtasio.annotations import (
    Color,
    FillStyle,
    HorizontalAlignment,
    StrokeStyle,
    VerticalAlignment,
    square_callout,
    text_callout,
)


class TestColor:
    """Test Color class for annotations."""

    def test_color_creation(self):
        """Test basic Color creation."""
        color = Color(0.5, 0.6, 0.7, 0.8)
        assert color.red == 0.5
        assert color.green == 0.6
        assert color.blue == 0.7
        assert color.opacity == 0.8

    def test_color_default_opacity(self):
        """Test Color with default opacity."""
        color = Color(0.1, 0.2, 0.3)
        assert color.opacity == 1.0

    def test_color_validation(self):
        """Test Color value validation."""
        # Test red out of range
        with pytest.raises(ValueError, match="red.*out of range"):
            Color(1.1, 0.5, 0.5)

        with pytest.raises(ValueError, match="red.*out of range"):
            Color(-0.1, 0.5, 0.5)

        # Test green out of range
        with pytest.raises(ValueError, match="green.*out of range"):
            Color(0.5, 1.1, 0.5)

        # Test blue out of range
        with pytest.raises(ValueError, match="blue.*out of range"):
            Color(0.5, 0.5, 1.1)

        # Test opacity out of range
        with pytest.raises(ValueError, match="opacity.*out of range"):
            Color(0.5, 0.5, 0.5, 1.1)

    def test_color_from_rgb(self):
        """Test creating Color from RGB values."""
        color = Color.from_rgb(255, 128, 64, 32)
        assert color.red == 1.0
        assert color.green == 128 / 255
        assert color.blue == 64 / 255
        assert color.opacity == 32 / 255

    def test_color_from_hex(self):
        """Test creating Color from hex string."""
        color = Color.from_hex("#FF8040")
        assert color.red == 1.0
        assert color.green == 128 / 255
        assert color.blue == 64 / 255
        assert color.opacity == 1.0

        color = Color.from_hex("#FF804020")
        assert color.red == 1.0
        assert color.green == 128 / 255
        assert color.blue == 64 / 255
        assert color.opacity == 32 / 255

    def test_color_to_rgb(self):
        """Test converting Color to RGB tuple."""
        color = Color(1.0, 0.5, 0.25, 0.125)
        rgb = color.to_rgb()
        assert rgb == (255, 127, 63, 31)

    def test_color_presets(self):
        """Test Color preset methods."""
        white = Color.white()
        assert white == Color(1.0, 1.0, 1.0, 1.0)

        black = Color.black()
        assert black == Color(0.0, 0.0, 0.0, 1.0)

        transparent = Color.transparent()
        assert transparent == Color(0.0, 0.0, 0.0, 0.0)


class TestEnums:
    """Test annotation enum classes."""

    def test_horizontal_alignment(self):
        """Test HorizontalAlignment enum."""
        assert HorizontalAlignment.LEFT == "left"
        assert HorizontalAlignment.CENTER == "center"
        assert HorizontalAlignment.RIGHT == "right"

    def test_vertical_alignment(self):
        """Test VerticalAlignment enum."""
        assert VerticalAlignment.TOP == "top"
        assert VerticalAlignment.CENTER == "center"
        assert VerticalAlignment.BOTTOM == "bottom"

    def test_fill_style(self):
        """Test FillStyle enum."""
        assert FillStyle.SOLID == "solid"
        assert FillStyle.GRADIENT == "gradient"

    def test_stroke_style(self):
        """Test StrokeStyle enum."""
        assert StrokeStyle.SOLID == "solid"
        assert StrokeStyle.DASH == "dash"
        assert StrokeStyle.DOT == "dot"
        assert StrokeStyle.DASH_DOT == "dashdot"
        assert StrokeStyle.DASH_DOT_DOT == "dashdotdot"


class TestTextCallout:
    """Test text callout creation."""

    def test_text_callout_basic(self):
        """Test basic text callout creation."""
        callout = text_callout(text="Hello World", font_name="Arial", font_weight="normal")

        assert callout["kind"] == "remix"
        assert callout["shape"] == "text"
        assert callout["style"] == "basic"
        assert callout["text"] == "Hello World"
        assert callout["font"]["name"] == "Arial"
        assert callout["font"]["weight"] == "normal"

    def test_text_callout_with_custom_parameters(self):
        """Test text callout with custom parameters."""
        font_color = Color(1.0, 0.5, 0.0, 0.8)

        callout = text_callout(
            text="Custom Text",
            font_name="Times",
            font_weight="bold",
            font_size=72.0,
            font_color=font_color,
            height=300.0,
            width=500.0,
            horizontal_alignment=HorizontalAlignment.LEFT,
            vertical_alignment=VerticalAlignment.TOP,
            line_spacing=1.5,
        )

        assert callout["text"] == "Custom Text"
        assert callout["font"]["name"] == "Times"
        assert callout["font"]["weight"] == "bold"
        assert callout["font"]["size"] == 72.0
        assert callout["font"]["color-red"] == 1.0
        assert callout["font"]["color-green"] == 0.5
        assert callout["font"]["color-blue"] == 0.0
        assert callout["height"] == 300.0
        assert callout["width"] == 500.0
        assert callout["horizontal-alignment"] == "left"
        assert callout["vertical-alignment"] == "top"
        assert callout["line-spacing"] == 1.5

    def test_text_callout_default_color(self):
        """Test text callout with default white color."""
        callout = text_callout(text="Test", font_name="Arial", font_weight="normal")

        # Should use white color by default
        assert callout["font"]["color-red"] == 1.0
        assert callout["font"]["color-green"] == 1.0
        assert callout["font"]["color-blue"] == 1.0

    def test_text_callout_text_attributes(self):
        """Test text callout text attributes structure."""
        callout = text_callout(text="Test", font_name="Arial", font_weight="normal")

        assert "textAttributes" in callout
        assert callout["textAttributes"]["type"] == "textAttributeList"
        assert "keyframes" in callout["textAttributes"]
        assert len(callout["textAttributes"]["keyframes"]) == 1

        keyframe = callout["textAttributes"]["keyframes"][0]
        assert keyframe["endTime"] == 0
        assert keyframe["time"] == 0
        assert keyframe["value"] is None
        assert keyframe["duration"] == 0


class TestSquareCallout:
    """Test square callout creation."""

    def test_square_callout_basic(self):
        """Test basic square callout creation."""
        callout = square_callout(text="Square Text", font_name="Arial", font_weight="normal")

        assert callout["kind"] == "remix"
        assert callout["shape"] == "text-rectangle"
        assert callout["style"] == "basic"
        assert callout["text"] == "Square Text"
        assert callout["font"]["name"] == "Arial"
        assert callout["font"]["weight"] == "normal"

    def test_square_callout_with_custom_parameters(self):
        """Test square callout with all custom parameters."""
        font_color = Color(0.2, 0.3, 0.4, 0.9)
        fill_color = Color(0.8, 0.9, 1.0, 0.7)
        stroke_color = Color(0.1, 0.2, 0.3, 0.8)

        callout = square_callout(
            text="Custom Square",
            font_name="Helvetica",
            font_weight="bold",
            font_size=48.0,
            font_color=font_color,
            fill_color=fill_color,
            fill_style=FillStyle.GRADIENT,
            stroke_color=stroke_color,
            stroke_width=3.0,
            stroke_style=StrokeStyle.DASH,
            height=200.0,
            width=400.0,
            horizontal_alignment=HorizontalAlignment.RIGHT,
            vertical_alignment=VerticalAlignment.BOTTOM,
            line_spacing=2.0,
            tail_x=10.0,
            tail_y=-30.0,
        )

        assert callout["text"] == "Custom Square"
        assert callout["font"]["name"] == "Helvetica"
        assert callout["font"]["weight"] == "bold"
        assert callout["font"]["size"] == 48.0

        # Font color
        assert callout["font"]["color-red"] == 0.2
        assert callout["font"]["color-green"] == 0.3
        assert callout["font"]["color-blue"] == 0.4
        assert callout["font"]["color-opacity"] == 0.9

        # Fill color
        assert callout["fill-color-red"] == 0.8
        assert callout["fill-color-green"] == 0.9
        assert callout["fill-color-blue"] == 1.0
        assert callout["fill-color-opacity"] == 0.7

        # Stroke color
        assert callout["stroke-color-red"] == 0.1
        assert callout["stroke-color-green"] == 0.2
        assert callout["stroke-color-blue"] == 0.3
        assert callout["stroke-color-opacity"] == 0.8

        # Styles
        assert callout["fill-style"] == "gradient"
        assert callout["stroke-style"] == "dash"
        assert callout["stroke-width"] == 3.0

        # Dimensions and positioning
        assert callout["height"] == 200.0
        assert callout["width"] == 400.0
        assert callout["horizontal-alignment"] == "right"
        assert callout["vertical-alignment"] == "bottom"
        assert callout["line-spacing"] == 2.0
        assert callout["tail-x"] == 10.0
        assert callout["tail-y"] == -30.0

    def test_square_callout_default_colors(self):
        """Test square callout with default colors."""
        callout = square_callout(text="Test", font_name="Arial", font_weight="normal")

        # Font color should default to black
        assert callout["font"]["color-red"] == 0.0
        assert callout["font"]["color-green"] == 0.0
        assert callout["font"]["color-blue"] == 0.0
        assert callout["font"]["color-opacity"] == 1.0

        # Fill color should default to white
        assert callout["fill-color-red"] == 1.0
        assert callout["fill-color-green"] == 1.0
        assert callout["fill-color-blue"] == 1.0
        assert callout["fill-color-opacity"] == 1.0

        # Stroke color should default to teal
        assert callout["stroke-color-red"] == 0.0
        assert callout["stroke-color-green"] == 0.5
        assert callout["stroke-color-blue"] == 0.5
        assert callout["stroke-color-opacity"] == 1.0

    def test_square_callout_tail_positioning(self):
        """Test square callout tail positioning."""
        callout = square_callout(
            text="Test", font_name="Arial", font_weight="normal", tail_x=5.0, tail_y=-10.0
        )

        assert callout["tail-x"] == 5.0
        assert callout["tail-y"] == -10.0

    def test_square_callout_text_attributes(self):
        """Test square callout text attributes structure."""
        callout = square_callout(text="Test", font_name="Arial", font_weight="normal")

        assert "textAttributes" in callout
        assert callout["textAttributes"]["type"] == "textAttributeList"
        assert "keyframes" in callout["textAttributes"]
        assert len(callout["textAttributes"]["keyframes"]) == 1


class TestCalloutDataStructure:
    """Test callout data structure validity."""

    def test_text_callout_required_fields(self):
        """Test that text callout has all required fields."""
        callout = text_callout("Test", "Arial", "normal")

        required_fields = [
            "kind",
            "shape",
            "style",
            "height",
            "width",
            "text",
            "horizontal-alignment",
            "vertical-alignment",
            "font",
            "textAttributes",
            "line-spacing",
            "word-wrap",
            "resize-behavior",
        ]

        for field in required_fields:
            assert field in callout, f"Missing required field: {field}"

        # Font should have required subfields
        font_fields = [
            "color-red",
            "color-green",
            "color-blue",
            "size",
            "name",
            "weight",
            "tracking",
        ]
        for field in font_fields:
            assert field in callout["font"], f"Missing font field: {field}"

    def test_square_callout_required_fields(self):
        """Test that square callout has all required fields."""
        callout = square_callout("Test", "Arial", "normal")

        required_fields = [
            "kind",
            "shape",
            "style",
            "height",
            "width",
            "text",
            "horizontal-alignment",
            "vertical-alignment",
            "font",
            "textAttributes",
            "line-spacing",
            "word-wrap",
            "resize-behavior",
            "fill-color-red",
            "fill-color-green",
            "fill-color-blue",
            "fill-color-opacity",
            "stroke-color-red",
            "stroke-color-green",
            "stroke-color-blue",
            "stroke-color-opacity",
            "stroke-width",
            "fill-style",
            "stroke-style",
            "tail-x",
            "tail-y",
        ]

        for field in required_fields:
            assert field in callout, f"Missing required field: {field}"


class TestAnnotationBoundaryValues:
    """Test annotations with boundary and edge case values."""

    def test_color_boundary_values(self):
        """Test Color with boundary values."""
        # Minimum values
        color_min = Color(0.0, 0.0, 0.0, 0.0)
        assert color_min.red == 0.0
        assert color_min.opacity == 0.0

        # Maximum values
        color_max = Color(1.0, 1.0, 1.0, 1.0)
        assert color_max.red == 1.0
        assert color_max.opacity == 1.0

    def test_callout_extreme_dimensions(self):
        """Test callouts with extreme dimensions."""
        # Very small dimensions
        callout = text_callout("Test", "Arial", "normal", height=1.0, width=1.0, font_size=1.0)
        assert callout["height"] == 1.0
        assert callout["width"] == 1.0
        assert callout["font"]["size"] == 1.0

        # Very large dimensions
        callout = text_callout(
            "Test", "Arial", "normal", height=10000.0, width=10000.0, font_size=1000.0
        )
        assert callout["height"] == 10000.0
        assert callout["width"] == 10000.0
        assert callout["font"]["size"] == 1000.0

    def test_callout_string_types(self):
        """Test callouts handle various string types."""
        # Empty string
        callout = text_callout("", "Arial", "normal")
        assert callout["text"] == ""

        # Unicode string
        callout = text_callout("🎬 Video Title", "Arial", "normal")
        assert callout["text"] == "🎬 Video Title"

        # Long string
        long_text = "A" * 1000
        callout = text_callout(long_text, "Arial", "normal")
        assert callout["text"] == long_text


class TestAnnotationEdgeCases:
    """Test annotations with extreme edge cases and malformed inputs."""

    def test_color_nan_values(self):
        """Test Color behavior with NaN values."""

        # NaN values should raise ValueError
        with pytest.raises(ValueError, match="red.*out of range"):
            Color(float("nan"), 0.5, 0.5)

        with pytest.raises(ValueError, match="green.*out of range"):
            Color(0.5, float("nan"), 0.5)

        with pytest.raises(ValueError, match="blue.*out of range"):
            Color(0.5, 0.5, float("nan"))

        with pytest.raises(ValueError, match="opacity.*out of range"):
            Color(0.5, 0.5, 0.5, float("nan"))

    def test_color_infinity_values(self):
        """Test Color behavior with infinity values."""
        # Positive infinity should be out of range
        with pytest.raises(ValueError, match="red.*out of range"):
            Color(float("inf"), 0.5, 0.5)

        with pytest.raises(ValueError, match="green.*out of range"):
            Color(0.5, float("inf"), 0.5)

        # Negative infinity should also be out of range
        with pytest.raises(ValueError, match="blue.*out of range"):
            Color(0.5, 0.5, float("-inf"))

        with pytest.raises(ValueError, match="opacity.*out of range"):
            Color(0.5, 0.5, 0.5, float("-inf"))

    def test_color_invalid_types(self):
        """Test Color with invalid data types."""
        # String values that can't be converted
        with pytest.raises((ValueError, TypeError)):
            Color("invalid", 0.5, 0.5)

        with pytest.raises((ValueError, TypeError)):
            Color(0.5, "not_a_number", 0.5)

        # None values
        with pytest.raises((ValueError, TypeError)):
            Color(None, 0.5, 0.5)

        # List/dict values
        with pytest.raises((ValueError, TypeError)):
            Color([0.5], 0.5, 0.5)

    def test_color_from_rgb_extreme_values(self):
        """Test Color.from_rgb with extreme values."""
        # Values way out of range
        with pytest.raises(ValueError, match="out of range"):
            Color.from_rgb(999, 128, 64)

        with pytest.raises(ValueError, match="out of range"):
            Color.from_rgb(255, -999, 64)

        with pytest.raises(ValueError, match="out of range"):
            Color.from_rgb(255, 128, 256)

    def test_color_from_hex_malformed(self):
        """Test Color.from_hex with malformed hex strings."""
        # Invalid hex characters
        with pytest.raises(ValueError):
            Color.from_hex("#GGG")

        # Invalid lengths
        with pytest.raises(ValueError, match="Invalid hex color format"):
            Color.from_hex("#12")

        with pytest.raises(ValueError, match="Invalid hex color format"):
            Color.from_hex("#12345")

        # Empty string
        with pytest.raises(ValueError, match="Invalid hex color format"):
            Color.from_hex("")

        # None value
        with pytest.raises((ValueError, TypeError, AttributeError)):
            Color.from_hex(None)

    def test_callout_parameter_type_coercion(self):
        """Test callouts handle parameter type coercion gracefully."""
        # Integer text should be converted to string
        callout = text_callout(123, "Arial", "normal")
        assert callout["text"] == "123"

        # Integer font name should be converted to string
        callout = text_callout("Test", 123, "normal")
        assert callout["font"]["name"] == "123"

        # Integer font weight should be converted to string
        callout = text_callout("Test", "Arial", 123)
        assert callout["font"]["weight"] == "123"

        # Test that None values are handled gracefully (converted to "None" string)
        callout = text_callout(None, "Arial", "normal")
        assert callout["text"] == "None"

    def test_callout_negative_dimensions(self):
        """Test callouts with negative dimensions."""
        # Negative dimensions should be handled gracefully or raise appropriate errors
        callout = text_callout(
            "Test", "Arial", "normal", height=-100.0, width=-200.0, font_size=-10.0
        )
        # Should either accept negative values or use absolute values
        assert callout["height"] == -100.0 or callout["height"] == 100.0
        assert callout["width"] == -200.0 or callout["width"] == 200.0
        assert callout["font"]["size"] == -10.0 or callout["font"]["size"] == 10.0

    def test_callout_zero_dimensions(self):
        """Test callouts with zero dimensions."""
        callout = text_callout("Test", "Arial", "normal", height=0.0, width=0.0, font_size=0.0)
        assert callout["height"] == 0.0
        assert callout["width"] == 0.0
        assert callout["font"]["size"] == 0.0

    def test_square_callout_extreme_tail_positions(self):
        """Test square callout with extreme tail positions."""
        # Very large positive values
        callout = square_callout("Test", "Arial", "normal", tail_x=999999.0, tail_y=888888.0)
        assert callout["tail-x"] == 999999.0
        assert callout["tail-y"] == 888888.0

        # Very large negative values
        callout = square_callout("Test", "Arial", "normal", tail_x=-999999.0, tail_y=-888888.0)
        assert callout["tail-x"] == -999999.0
        assert callout["tail-y"] == -888888.0

    def test_callout_special_characters_in_text(self):
        """Test callouts with special characters and control characters."""
        # Newlines and tabs
        callout = text_callout("Line 1\nLine 2\tTabbed", "Arial", "normal")
        assert callout["text"] == "Line 1\nLine 2\tTabbed"

        # Control characters
        callout = text_callout("Control\x00\x01\x02", "Arial", "normal")
        assert callout["text"] == "Control\x00\x01\x02"

        # HTML/XML special characters
        callout = text_callout("<>&\"'", "Arial", "normal")
        assert callout["text"] == "<>&\"'"
