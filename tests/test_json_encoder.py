# this_file: tests/test_json_encoder.py
"""Tests for custom JSON encoder."""

import json
import math

import pytest

from camtasio.serialization.json_encoder import CamtasiaJSONEncoder


class TestCamtasiaJSONEncoder:
    """Test CamtasiaJSONEncoder class."""

    @pytest.fixture
    def encoder(self):
        """Create encoder instance."""
        return CamtasiaJSONEncoder()

    def test_encode_normal_values(self, encoder):
        """Test encoding normal values."""
        data = {
            "string": "hello",
            "integer": 42,
            "float": 3.14,
            "boolean": True,
            "null": None,
            "array": [1, 2, 3],
            "nested": {"key": "value"}
        }

        result = encoder.encode(data)

        # Should be valid JSON
        parsed = json.loads(result)
        assert parsed["string"] == "hello"
        assert parsed["integer"] == 42
        assert parsed["float"] == 3.14
        assert parsed["boolean"] is True
        assert parsed["null"] is None
        assert parsed["array"] == [1, 2, 3]
        assert parsed["nested"]["key"] == "value"

    def test_encode_positive_infinity(self, encoder):
        """Test encoding positive infinity."""
        data = {"value": float('inf')}

        result = encoder.encode(data)
        parsed = json.loads(result)

        # Should convert to maximum safe float
        assert parsed["value"] == -encoder.MIN_SAFE_FLOAT

    def test_encode_negative_infinity(self, encoder):
        """Test encoding negative infinity."""
        data = {"value": float('-inf')}

        result = encoder.encode(data)
        parsed = json.loads(result)

        # Should convert to minimum safe float
        assert parsed["value"] == encoder.MIN_SAFE_FLOAT

    def test_encode_nan(self, encoder):
        """Test encoding NaN."""
        data = {"value": float('nan')}

        result = encoder.encode(data)
        parsed = json.loads(result)

        # Should convert to 0.0
        assert parsed["value"] == 0.0

    def test_encode_nested_special_values(self, encoder):
        """Test encoding nested structures with special values."""
        data = {
            "level1": {
                "level2": {
                    "inf": float('inf'),
                    "neg_inf": float('-inf'),
                    "nan": float('nan'),
                    "normal": 42.5
                },
                "array": [float('inf'), float('-inf'), float('nan'), 1.0]
            }
        }

        result = encoder.encode(data)
        parsed = json.loads(result)

        # Check nested dictionary values
        level2 = parsed["level1"]["level2"]
        assert level2["inf"] == -encoder.MIN_SAFE_FLOAT
        assert level2["neg_inf"] == encoder.MIN_SAFE_FLOAT
        assert level2["nan"] == 0.0
        assert level2["normal"] == 42.5

        # Check array values
        array = parsed["level1"]["array"]
        assert array[0] == -encoder.MIN_SAFE_FLOAT  # +inf
        assert array[1] == encoder.MIN_SAFE_FLOAT   # -inf
        assert array[2] == 0.0                      # nan
        assert array[3] == 1.0                      # normal

    def test_encode_array_of_special_values(self, encoder):
        """Test encoding array containing only special float values."""
        data = [float('inf'), float('-inf'), float('nan')]

        result = encoder.encode(data)
        parsed = json.loads(result)

        assert len(parsed) == 3
        assert parsed[0] == -encoder.MIN_SAFE_FLOAT  # +inf
        assert parsed[1] == encoder.MIN_SAFE_FLOAT   # -inf
        assert parsed[2] == 0.0                      # nan

    def test_encode_mixed_types_with_special_floats(self, encoder):
        """Test encoding mixed data types including special floats."""
        data = {
            "string": "test",
            "int": 100,
            "normal_float": 3.14159,
            "inf": float('inf'),
            "neg_inf": float('-inf'),
            "nan": float('nan'),
            "array": ["text", 42, float('inf')],
            "nested": {
                "bool": True,
                "special": float('nan')
            }
        }

        result = encoder.encode(data)
        parsed = json.loads(result)

        # Regular values should be unchanged
        assert parsed["string"] == "test"
        assert parsed["int"] == 100
        assert parsed["normal_float"] == 3.14159
        assert parsed["nested"]["bool"] is True

        # Special values should be converted
        assert parsed["inf"] == -encoder.MIN_SAFE_FLOAT
        assert parsed["neg_inf"] == encoder.MIN_SAFE_FLOAT
        assert parsed["nan"] == 0.0
        assert parsed["array"][2] == -encoder.MIN_SAFE_FLOAT
        assert parsed["nested"]["special"] == 0.0

    def test_iterencode_special_values(self, encoder):
        """Test iterencode method with special values."""
        data = {"inf": float('inf'), "normal": 42}

        # Collect all chunks from iterator
        chunks = list(encoder.iterencode(data))
        result = ''.join(chunks)

        parsed = json.loads(result)
        assert parsed["inf"] == -encoder.MIN_SAFE_FLOAT
        assert parsed["normal"] == 42

    def test_iterencode_one_shot(self, encoder):
        """Test iterencode with _one_shot parameter."""
        data = {"value": float('nan')}

        # Test with _one_shot=True
        chunks = list(encoder.iterencode(data, _one_shot=True))
        result = ''.join(chunks)

        parsed = json.loads(result)
        assert parsed["value"] == 0.0

    def test_preprocess_method_directly(self, encoder):
        """Test _preprocess method directly."""
        # Test float preprocessing
        assert encoder._preprocess(3.14) == 3.14
        assert encoder._preprocess(float('inf')) == -encoder.MIN_SAFE_FLOAT
        assert encoder._preprocess(float('-inf')) == encoder.MIN_SAFE_FLOAT
        assert encoder._preprocess(float('nan')) == 0.0

        # Test dict preprocessing
        input_dict = {"inf": float('inf'), "normal": 42}
        result_dict = encoder._preprocess(input_dict)
        assert result_dict["inf"] == -encoder.MIN_SAFE_FLOAT
        assert result_dict["normal"] == 42

        # Test list preprocessing
        input_list = [float('nan'), 1.0, float('-inf')]
        result_list = encoder._preprocess(input_list)
        assert result_list[0] == 0.0
        assert result_list[1] == 1.0
        assert result_list[2] == encoder.MIN_SAFE_FLOAT

        # Test non-numeric types (should pass through unchanged)
        assert encoder._preprocess("string") == "string"
        assert encoder._preprocess(True) is True
        assert encoder._preprocess(None) is None

    def test_min_safe_float_constant(self, encoder):
        """Test MIN_SAFE_FLOAT constant value."""
        # Should be a very large negative float
        assert encoder.MIN_SAFE_FLOAT < 0
        assert encoder.MIN_SAFE_FLOAT == -1.7976931348623157e308

        # Should be finite
        assert math.isfinite(encoder.MIN_SAFE_FLOAT)
        assert not math.isinf(encoder.MIN_SAFE_FLOAT)
        assert not math.isnan(encoder.MIN_SAFE_FLOAT)

    def test_complex_nested_structure(self, encoder):
        """Test encoding deeply nested structure with special values."""
        data = {
            "project": {
                "timeline": {
                    "tracks": [
                        {
                            "id": 1,
                            "media": {
                                "position": {
                                    "x": float('inf'),  # This might happen in buggy projects
                                    "y": float('-inf'),
                                    "z": float('nan')
                                },
                                "scale": 1.0,
                                "rotation": 0.0
                            },
                            "effects": [
                                {
                                    "type": "blur",
                                    "intensity": float('nan'),  # Invalid effect value
                                    "enabled": True
                                }
                            ]
                        }
                    ]
                }
            }
        }

        result = encoder.encode(data)
        parsed = json.loads(result)

        # Navigate to the position object
        position = parsed["project"]["timeline"]["tracks"][0]["media"]["position"]
        assert position["x"] == -encoder.MIN_SAFE_FLOAT  # +inf converted
        assert position["y"] == encoder.MIN_SAFE_FLOAT   # -inf converted
        assert position["z"] == 0.0                      # nan converted

        # Check other values are preserved
        media = parsed["project"]["timeline"]["tracks"][0]["media"]
        assert media["scale"] == 1.0
        assert media["rotation"] == 0.0

        # Check effects
        effect = parsed["project"]["timeline"]["tracks"][0]["effects"][0]
        assert effect["type"] == "blur"
        assert effect["intensity"] == 0.0  # nan converted
        assert effect["enabled"] is True

    def test_empty_structures(self, encoder):
        """Test encoding empty structures."""
        # Empty dict
        assert encoder.encode({}) == "{}"

        # Empty list
        assert encoder.encode([]) == "[]"

        # Dict with empty nested structures
        data = {"empty_dict": {}, "empty_list": []}
        result = encoder.encode(data)
        parsed = json.loads(result)
        assert parsed["empty_dict"] == {}
        assert parsed["empty_list"] == []

    def test_large_numbers(self, encoder):
        """Test encoding very large but finite numbers."""
        data = {
            "large_positive": 1e100,
            "large_negative": -1e100,
            "very_small": 1e-100
        }

        result = encoder.encode(data)
        parsed = json.loads(result)

        # Should preserve large finite numbers
        assert parsed["large_positive"] == 1e100
        assert parsed["large_negative"] == -1e100
        assert parsed["very_small"] == 1e-100

    def test_zero_and_negative_zero(self, encoder):
        """Test encoding zero and negative zero."""
        data = {
            "zero": 0.0,
            "negative_zero": -0.0
        }

        result = encoder.encode(data)
        parsed = json.loads(result)

        # Both should be preserved (though JSON doesn't distinguish -0.0)
        assert parsed["zero"] == 0.0
        assert parsed["negative_zero"] == 0.0  # -0.0 becomes 0.0 in JSON
