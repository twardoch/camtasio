#!/usr/bin/env python3
"""Comprehensive tests for the effects system."""
# this_file: tests/test_effects_new.py

import pytest

from camtasio.effects import ChromaKeyEffect, Effect, VisualEffect
from camtasio.utils import RGBA


class TestRGBA:
    """Test RGBA color utility class."""

    def test_rgba_creation(self):
        """Test basic RGBA creation."""
        color = RGBA(255, 128, 64, 32)
        assert color.red == 255
        assert color.green == 128
        assert color.blue == 64
        assert color.alpha == 32

    def test_rgba_validation(self):
        """Test RGBA value validation."""
        with pytest.raises(ValueError, match="out of range"):
            RGBA(256, 0, 0, 255)  # red too high

        with pytest.raises(ValueError, match="out of range"):
            RGBA(0, -1, 0, 255)  # green too low

    def test_rgba_from_hex(self):
        """Test creating RGBA from hex strings."""
        # 6-digit hex
        color = RGBA.from_hex("#FF8040")
        assert color.red == 255
        assert color.green == 128
        assert color.blue == 64
        assert color.alpha == 255

        # 8-digit hex with alpha
        color = RGBA.from_hex("#FF804020")
        assert color.red == 255
        assert color.green == 128
        assert color.blue == 64
        assert color.alpha == 32

        # 3-digit hex
        color = RGBA.from_hex("#F84")
        assert color.red == 255
        assert color.green == 136
        assert color.blue == 68
        assert color.alpha == 255

    def test_rgba_from_floats(self):
        """Test creating RGBA from float values."""
        color = RGBA.from_floats(1.0, 0.5, 0.25, 0.125)
        assert color.red == 255
        assert color.green == 127
        assert color.blue == 63
        assert color.alpha == 31

    def test_rgba_as_floats(self):
        """Test converting RGBA to float values."""
        color = RGBA(255, 128, 64, 32)
        floats = color.as_floats()
        assert floats == (1.0, 128 / 255, 64 / 255, 32 / 255)

    def test_rgba_to_hex(self):
        """Test converting RGBA to hex string."""
        color = RGBA(255, 128, 64, 255)
        assert color.to_hex() == "#FF8040"

        color = RGBA(255, 128, 64, 32)
        assert color.to_hex() == "#FF804020"
        assert color.to_hex(include_alpha=False) == "#FF8040"


class TestChromaKeyEffect:
    """Test ChromaKey effect class."""

    def test_chromakey_creation_default(self):
        """Test default ChromaKey creation."""
        effect = ChromaKeyEffect()
        assert effect.name == "ChromaKey"
        assert effect.category == "categoryVisualEffects"
        assert effect.tolerance == 0.1
        assert effect.softness == 0.1
        assert effect.defringe == 0.0
        assert effect.compensation == 0.0
        assert effect.inverted is False
        assert effect.hue == RGBA(0, 255, 0, 255)  # Default green

    def test_chromakey_creation_with_parameters(self):
        """Test ChromaKey creation with custom parameters."""
        hue = RGBA(255, 0, 0, 255)  # Red
        effect = ChromaKeyEffect(
            tolerance=0.2, softness=0.3, defringe=0.1, compensation=0.5, inverted=True, hue=hue
        )

        assert effect.tolerance == 0.2
        assert effect.softness == 0.3
        assert effect.defringe == 0.1
        assert effect.compensation == 0.5
        assert effect.inverted is True
        assert effect.hue == hue

    def test_chromakey_creation_with_hex_color(self):
        """Test ChromaKey creation with hex color string."""
        effect = ChromaKeyEffect(hue="#FF0000")
        assert effect.hue == RGBA(255, 0, 0, 255)

    def test_chromakey_parameter_validation(self):
        """Test ChromaKey parameter validation."""
        # Test tolerance validation
        with pytest.raises(ValueError, match="tolerance.*out of range"):
            ChromaKeyEffect(tolerance=-0.1)

        with pytest.raises(ValueError, match="tolerance.*out of range"):
            ChromaKeyEffect(tolerance=1.1)

        # Test softness validation
        with pytest.raises(ValueError, match="softness.*out of range"):
            ChromaKeyEffect(softness=-0.1)

        with pytest.raises(ValueError, match="softness.*out of range"):
            ChromaKeyEffect(softness=1.1)

        # Test defringe validation
        with pytest.raises(ValueError, match="defringe.*out of range"):
            ChromaKeyEffect(defringe=-1.1)

        with pytest.raises(ValueError, match="defringe.*out of range"):
            ChromaKeyEffect(defringe=1.1)

        # Test compensation validation
        with pytest.raises(ValueError, match="compensation.*out of range"):
            ChromaKeyEffect(compensation=-0.1)

        with pytest.raises(ValueError, match="compensation.*out of range"):
            ChromaKeyEffect(compensation=1.1)

    def test_chromakey_color_properties(self):
        """Test ChromaKey normalized color properties."""
        effect = ChromaKeyEffect(hue=RGBA(255, 128, 64, 32))

        assert effect.red == 1.0
        assert effect.green == 128 / 255
        assert effect.blue == 64 / 255
        assert effect.alpha == 32 / 255

    def test_chromakey_parameters_dict(self):
        """Test ChromaKey parameters dictionary."""
        effect = ChromaKeyEffect(
            tolerance=0.2,
            softness=0.3,
            defringe=0.1,
            compensation=0.5,
            inverted=True,
            hue=RGBA(255, 128, 64, 32),
        )

        params = effect.parameters
        expected = {
            "clrCompensation": 0.5,
            "color-alpha": 32 / 255,
            "color-red": 1.0,
            "color-green": 128 / 255,
            "color-blue": 64 / 255,
            "defringe": 0.1,
            "enabled": 1,
            "invertEffect": 1.0,  # True converted to float
            "softness": 0.3,
            "tolerance": 0.2,
        }

        assert params == expected

    def test_chromakey_metadata(self):
        """Test ChromaKey metadata generation."""
        effect = ChromaKeyEffect()
        metadata = effect.metadata

        # Should contain default values
        assert "default-ChromaKey-color" in metadata
        assert "default-ChromaKey-defringe" in metadata
        assert "default-ChromaKey-invertEffect" in metadata
        assert "default-ChromaKey-softness" in metadata
        assert "default-ChromaKey-tolerance" in metadata
        assert "default-ChromaKey-clrCompensation" in metadata

    def test_chromakey_from_dict(self):
        """Test creating ChromaKey from dictionary data."""
        data = {
            "effectName": "ChromaKey",
            "category": "categoryVisualEffects",
            "parameters": {
                "tolerance": 0.2,
                "softness": 0.3,
                "defringe": 0.1,
                "clrCompensation": 0.5,
                "invertEffect": 1.0,
                "color-red": 1.0,
                "color-green": 0.5,
                "color-blue": 0.25,
                "color-alpha": 0.125,
            },
        }

        effect = ChromaKeyEffect.from_dict(data)

        assert effect.tolerance == 0.2
        assert effect.softness == 0.3
        assert effect.defringe == 0.1
        assert effect.compensation == 0.5
        assert effect.inverted is True
        assert effect.hue == RGBA.from_floats(1.0, 0.5, 0.25, 0.125)

    def test_chromakey_to_dict(self):
        """Test converting ChromaKey to dictionary."""
        effect = ChromaKeyEffect(
            tolerance=0.2,
            softness=0.3,
            defringe=0.1,
            compensation=0.5,
            inverted=True,
            hue=RGBA(255, 128, 64, 32),
        )

        data = effect.to_dict()

        assert data["effectName"] == "ChromaKey"
        assert data["category"] == "categoryVisualEffects"
        assert data["parameters"]["tolerance"] == 0.2
        assert data["parameters"]["softness"] == 0.3
        assert data["parameters"]["defringe"] == 0.1
        assert data["parameters"]["clrCompensation"] == 0.5
        assert data["parameters"]["invertEffect"] == 1.0

    def test_chromakey_roundtrip(self):
        """Test ChromaKey serialization roundtrip."""
        original = ChromaKeyEffect(
            tolerance=0.2,
            softness=0.3,
            defringe=0.1,
            compensation=0.5,
            inverted=True,
            hue=RGBA(255, 128, 64, 32),
        )

        # Serialize to dict
        data = original.to_dict()

        # Deserialize from dict
        restored = ChromaKeyEffect.from_dict(data)

        # Should be equivalent
        assert restored.tolerance == original.tolerance
        assert restored.softness == original.softness
        assert restored.defringe == original.defringe
        assert restored.compensation == original.compensation
        assert restored.inverted == original.inverted
        assert restored.hue == original.hue


class TestEffectBoundaryValues:
    """Test effects with boundary and edge case values."""

    def test_chromakey_minimum_values(self):
        """Test ChromaKey with minimum allowed values."""
        effect = ChromaKeyEffect(
            tolerance=0.0,
            softness=0.0,
            defringe=-1.0,
            compensation=0.0,
            inverted=False,
            hue=RGBA(0, 0, 0, 0),
        )

        assert effect.tolerance == 0.0
        assert effect.softness == 0.0
        assert effect.defringe == -1.0
        assert effect.compensation == 0.0
        assert effect.inverted is False

    def test_chromakey_maximum_values(self):
        """Test ChromaKey with maximum allowed values."""
        effect = ChromaKeyEffect(
            tolerance=1.0,
            softness=1.0,
            defringe=1.0,
            compensation=1.0,
            inverted=True,
            hue=RGBA(255, 255, 255, 255),
        )

        assert effect.tolerance == 1.0
        assert effect.softness == 1.0
        assert effect.defringe == 1.0
        assert effect.compensation == 1.0
        assert effect.inverted is True

    def test_rgba_boundary_values(self):
        """Test RGBA with boundary values."""
        # Minimum values
        color_min = RGBA(0, 0, 0, 0)
        assert color_min.as_floats() == (0.0, 0.0, 0.0, 0.0)

        # Maximum values
        color_max = RGBA(255, 255, 255, 255)
        assert color_max.as_floats() == (1.0, 1.0, 1.0, 1.0)


class TestEffectConstants:
    """Test effect constant values and ranges."""

    def test_chromakey_constants(self):
        """Test ChromaKey class constants."""
        assert ChromaKeyEffect.MINIMUM_TOLERANCE == 0.0
        assert ChromaKeyEffect.MAXIMUM_TOLERANCE == 1.0
        assert ChromaKeyEffect.MINIMUM_SOFTNESS == 0.0
        assert ChromaKeyEffect.MAXIMUM_SOFTNESS == 1.0
        assert ChromaKeyEffect.MINIMUM_DEFRINGE == -1.0
        assert ChromaKeyEffect.MAXIMUM_DEFRINGE == 1.0
        assert ChromaKeyEffect.MINIMUM_COMPENSATION == 0.0
        assert ChromaKeyEffect.MAXIMUM_COMPENSATION == 1.0

    def test_rgba_constants(self):
        """Test RGBA class constants."""
        assert RGBA.MINIMUM_CHANNEL == 0
        assert RGBA.MAXIMUM_CHANNEL == 255


class TestEffectEdgeCases:
    """Test effects with extreme edge cases and invalid values."""

    def test_chromakey_nan_values(self):
        """Test ChromaKey behavior with NaN values."""
        # NaN values don't satisfy range checks, so they should raise ValueError
        with pytest.raises(ValueError, match="tolerance.*out of range"):
            ChromaKeyEffect(tolerance=float("nan"))

        with pytest.raises(ValueError, match="softness.*out of range"):
            ChromaKeyEffect(softness=float("nan"))

        with pytest.raises(ValueError, match="defringe.*out of range"):
            ChromaKeyEffect(defringe=float("nan"))

        with pytest.raises(ValueError, match="compensation.*out of range"):
            ChromaKeyEffect(compensation=float("nan"))

    def test_chromakey_infinity_values(self):
        """Test ChromaKey behavior with infinity values."""
        # Positive infinity should be out of range
        with pytest.raises(ValueError, match="tolerance.*out of range|invalid"):
            ChromaKeyEffect(tolerance=float("inf"))

        with pytest.raises(ValueError, match="softness.*out of range|invalid"):
            ChromaKeyEffect(softness=float("inf"))

        with pytest.raises(ValueError, match="defringe.*out of range|invalid"):
            ChromaKeyEffect(defringe=float("inf"))

        with pytest.raises(ValueError, match="compensation.*out of range|invalid"):
            ChromaKeyEffect(compensation=float("inf"))

        # Negative infinity should also be out of range
        with pytest.raises(ValueError, match="tolerance.*out of range|invalid"):
            ChromaKeyEffect(tolerance=float("-inf"))

        with pytest.raises(ValueError, match="softness.*out of range|invalid"):
            ChromaKeyEffect(softness=float("-inf"))

    def test_chromakey_extreme_negative_values(self):
        """Test ChromaKey with extreme negative values."""
        # Most parameters don't accept negative values except defringe
        with pytest.raises(ValueError, match="tolerance.*out of range"):
            ChromaKeyEffect(tolerance=-999.0)

        with pytest.raises(ValueError, match="softness.*out of range"):
            ChromaKeyEffect(softness=-0.0001)  # Just below minimum

        with pytest.raises(ValueError, match="compensation.*out of range"):
            ChromaKeyEffect(compensation=-0.1)

        # Defringe accepts -1.0 to 1.0, so test extreme negative
        with pytest.raises(ValueError, match="defringe.*out of range"):
            ChromaKeyEffect(defringe=-1.1)

    def test_chromakey_extreme_positive_values(self):
        """Test ChromaKey with extreme positive values."""
        with pytest.raises(ValueError, match="tolerance.*out of range"):
            ChromaKeyEffect(tolerance=1.0001)  # Just above maximum

        with pytest.raises(ValueError, match="softness.*out of range"):
            ChromaKeyEffect(softness=999.0)

        with pytest.raises(ValueError, match="defringe.*out of range"):
            ChromaKeyEffect(defringe=1.1)

        with pytest.raises(ValueError, match="compensation.*out of range"):
            ChromaKeyEffect(compensation=10.0)

    def test_rgba_invalid_types(self):
        """Test RGBA with invalid data types."""
        # String values that can't be converted
        with pytest.raises((ValueError, TypeError)):
            RGBA("not_a_number", 128, 64, 255)

        with pytest.raises((ValueError, TypeError)):
            RGBA(255, "invalid", 64, 255)

        # None values
        with pytest.raises((ValueError, TypeError)):
            RGBA(None, 128, 64, 255)

        # List/dict values
        with pytest.raises((ValueError, TypeError)):
            RGBA([255], 128, 64, 255)

    def test_rgba_extreme_values(self):
        """Test RGBA with extreme values."""
        # Values way out of range
        with pytest.raises(ValueError, match="out of range"):
            RGBA(999, 128, 64, 255)

        with pytest.raises(ValueError, match="out of range"):
            RGBA(255, -999, 64, 255)

        with pytest.raises(ValueError, match="out of range"):
            RGBA(255, 128, 256, 255)

        with pytest.raises(ValueError, match="out of range"):
            RGBA(255, 128, 64, 300)

    def test_rgba_hex_invalid_formats(self):
        """Test RGBA.from_hex with invalid formats."""
        # Invalid hex strings from our plan
        with pytest.raises(ValueError):  # Invalid hex characters will cause int() to fail
            RGBA.from_hex("#GGG")

        with pytest.raises(ValueError, match="Invalid hex color format"):
            RGBA.from_hex("#12")  # Too short

        with pytest.raises(ValueError, match="Invalid hex color format"):
            RGBA.from_hex("#12345")  # Invalid length

        # Note: "FF0000" without # is actually valid - lstrip("#") handles it
        color = RGBA.from_hex("FF0000")  # This should work
        assert color.red == 255 and color.green == 0 and color.blue == 0

        with pytest.raises(ValueError, match="Invalid hex color format"):
            RGBA.from_hex("")  # Empty string

        with pytest.raises((ValueError, TypeError, AttributeError)):
            RGBA.from_hex(None)  # None value will cause AttributeError on .lstrip()


class TestEffectBaseClass:
    """Test Effect base class functionality."""

    def test_effect_base_creation(self):
        """Test Effect base class cannot be instantiated directly."""
        # Effect is likely abstract, so this should raise TypeError
        with pytest.raises(TypeError):
            Effect()

    def test_visual_effect_creation(self):
        """Test VisualEffect base class."""
        # VisualEffect might also be abstract
        with pytest.raises(TypeError):
            VisualEffect()

    def test_effect_metadata_structure(self):
        """Test effect metadata has required structure."""
        effect = ChromaKeyEffect()
        metadata = effect.metadata

        # Metadata should be a dictionary
        assert isinstance(metadata, dict)

        # Should contain default values for all parameters
        required_keys = {
            "default-ChromaKey-color",
            "default-ChromaKey-defringe",
            "default-ChromaKey-invertEffect",
            "default-ChromaKey-softness",
            "default-ChromaKey-tolerance",
            "default-ChromaKey-clrCompensation",
        }

        for key in required_keys:
            assert key in metadata, f"Missing metadata key: {key}"

    def test_effect_parameters_structure(self):
        """Test effect parameters have required structure."""
        effect = ChromaKeyEffect(
            tolerance=0.5,
            softness=0.3,
            defringe=0.1,
            compensation=0.2,
            inverted=True,
            hue=RGBA(128, 64, 32, 255),
        )

        params = effect.parameters

        # Parameters should be a dictionary
        assert isinstance(params, dict)

        # Should contain all expected parameters
        required_params = {
            "clrCompensation",
            "color-alpha",
            "color-red",
            "color-green",
            "color-blue",
            "defringe",
            "enabled",
            "invertEffect",
            "softness",
            "tolerance",
        }

        for param in required_params:
            assert param in params, f"Missing parameter: {param}"

        # All parameter values should be numeric
        for key, value in params.items():
            assert isinstance(value, int | float), f"Parameter {key} is not numeric: {value}"


class TestEffectSerializationEdgeCases:
    """Test effect serialization with edge cases."""

    def test_chromakey_from_dict_missing_parameters(self):
        """Test ChromaKey creation from dict with missing parameters."""
        # Minimal dict with missing optional parameters
        data = {
            "effectName": "ChromaKey",
            "category": "categoryVisualEffects",
            "parameters": {
                # Missing most parameters - should use defaults
                "tolerance": 0.2
            },
        }

        effect = ChromaKeyEffect.from_dict(data)

        # Should use default values for missing parameters
        assert effect.tolerance == 0.2
        assert effect.softness == 0.1  # Default
        assert effect.defringe == 0.0  # Default
        assert effect.compensation == 0.0  # Default
        assert effect.inverted is False  # Default

    def test_chromakey_from_dict_extra_parameters(self):
        """Test ChromaKey creation from dict with extra parameters."""
        data = {
            "effectName": "ChromaKey",
            "category": "categoryVisualEffects",
            "parameters": {
                "tolerance": 0.2,
                "softness": 0.3,
                "unknown_parameter": 999,  # Should be ignored
                "another_extra": "invalid",  # Should be ignored
            },
        }

        # Should not raise error, just ignore extra parameters
        effect = ChromaKeyEffect.from_dict(data)
        assert effect.tolerance == 0.2
        assert effect.softness == 0.3

    def test_chromakey_from_dict_invalid_color_values(self):
        """Test ChromaKey creation with invalid color values in dict."""
        data = {
            "effectName": "ChromaKey",
            "category": "categoryVisualEffects",
            "parameters": {
                "tolerance": 0.2,
                "color-red": 2.0,  # Out of range (should be 0-1, will be converted to 510 which is > 255)
                "color-green": -0.5,  # Out of range (will be converted to negative)
                "color-blue": 0.5,
                "color-alpha": 1.0,
            },
        }

        # Should handle invalid color values gracefully - RGBA will validate range 0-255
        with pytest.raises(ValueError, match="RGBA.*channel.*out of range"):
            ChromaKeyEffect.from_dict(data)
