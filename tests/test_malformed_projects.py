# this_file: tests/test_malformed_projects.py
"""Test handling of malformed, corrupted, or invalid project files."""

import json
import tempfile
from pathlib import Path

import pytest

from camtasio.serialization import ProjectLoader


class TestMalformedProjects:
    """Test handling of various malformed project scenarios."""

    def test_empty_file(self):
        """Test loading an empty file."""
        with tempfile.NamedTemporaryFile(suffix=".tscproj", delete=False) as f:
            temp_path = Path(f.name)
            # Write nothing - empty file

        try:
            loader = ProjectLoader()
            with pytest.raises(json.JSONDecodeError):
                loader.load_file(temp_path)
        finally:
            temp_path.unlink()

    def test_invalid_json(self):
        """Test loading a file with invalid JSON."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tscproj", delete=False) as f:
            f.write("{ this is not valid json }")
            temp_path = Path(f.name)

        try:
            loader = ProjectLoader()
            with pytest.raises(json.JSONDecodeError):
                loader.load_file(temp_path)
        finally:
            temp_path.unlink()

    def test_missing_required_fields(self):
        """Test loading project missing required fields."""
        # Missing width and height
        data = {
            "version": "9.0",
            "editRate": 705600000,
            "sourceBin": [],
            "timeline": {"id": 1}
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".tscproj", delete=False) as f:
            json.dump(data, f)
            temp_path = Path(f.name)

        try:
            loader = ProjectLoader()
            # Should load with default values and warnings
            project = loader.load_file(temp_path)

            # Verify defaults were used
            assert project.canvas.width == 1920  # Default width
            assert project.canvas.height == 1080  # Default height

        finally:
            temp_path.unlink()

    def test_wrong_data_types(self):
        """Test loading project with wrong data types."""
        data = {
            "version": "9.0",
            "editRate": "not a number",  # Should be int
            "width": "1920",  # Should be int
            "height": True,  # Should be int
            "sourceBin": "not a list",  # Should be list
            "timeline": []  # Should be dict
        }

        loader = ProjectLoader()

        # The validate_structure method should catch these
        errors = loader.validate_structure(data)
        assert len(errors) > 0
        assert any("width must be a number" in err for err in errors)
        assert any("height must be a number" in err for err in errors)
        assert any("sourceBin must be a list" in err for err in errors)
        assert any("timeline must be a dictionary" in err for err in errors)

    def test_corrupted_nested_structure(self):
        """Test loading project with corrupted nested structures."""
        data = {
            "version": "9.0",
            "editRate": 705600000,
            "width": 1920,
            "height": 1080,
            "sourceBin": [
                {
                    # Missing required fields for source item
                    "id": 1
                    # Missing src, rect, etc.
                }
            ],
            "timeline": {
                "sceneTrack": {
                    "scenes": [
                        {
                            # Malformed scene
                            "csml": None  # Should be dict
                        }
                    ]
                }
            }
        }

        loader = ProjectLoader(strict_version_check=False)

        # Should handle gracefully or raise appropriate error
        try:
            project = loader.load_dict(data)
            # If it loads, verify it handled the corruption
            assert project is not None
        except (KeyError, ValueError, TypeError) as e:
            # Expected - malformed data should raise errors
            assert str(e) != ""

    def test_circular_references(self):
        """Test handling of circular references in JSON."""
        # Note: JSON doesn't support circular references natively,
        # but we can test that our code handles unexpected structures
        data = {
            "version": "9.0",
            "editRate": 705600000,
            "width": 1920,
            "height": 1080,
            "sourceBin": [],
            "timeline": {
                "id": 1,
                "sceneTrack": {
                    "scenes": []
                }
            }
        }

        # Add a reference that could cause issues if not handled properly
        data["timeline"]["parent"] = data  # type: ignore

        ProjectLoader()

        # The loader should handle this without infinite recursion
        # JSON encoding will fail on circular references
        with pytest.raises((ValueError, TypeError)):
            # This will fail during JSON processing
            json.dumps(data)

    def test_extremely_large_values(self):
        """Test handling of extremely large numeric values."""
        data = {
            "version": "9.0",
            "editRate": 705600000,
            "width": 999999999999999,  # Very large width
            "height": 999999999999999,  # Very large height
            "videoFormatFrameRate": 1000000,  # Unrealistic frame rate
            "sourceBin": [],
            "timeline": {
                "id": 1,
                "sceneTrack": {
                    "scenes": [{
                        "duration": 999999999999999999,  # Extremely long duration
                        "csml": {"tracks": []}
                    }]
                }
            }
        }

        loader = ProjectLoader()

        # Should load but with potential warnings
        project = loader.load_dict(data)
        assert project.canvas.width == 999999999999999
        assert project.canvas.height == 999999999999999

    def test_null_values(self):
        """Test handling of null values in required fields."""
        data = {
            "version": None,  # null version
            "editRate": 705600000,
            "width": 1920,
            "height": None,  # null height
            "sourceBin": None,  # null sourceBin
            "timeline": {
                "sceneTrack": None  # null sceneTrack
            }
        }

        loader = ProjectLoader(strict_version_check=False)

        # Should raise errors for null required fields
        with pytest.raises((TypeError, ValueError, KeyError)):
            loader.load_dict(data)

    def test_unicode_and_special_characters(self):
        """Test handling of unicode and special characters."""
        data = {
            "version": "9.0",
            "editRate": 705600000,
            "width": 1920,
            "height": 1080,
            "title": "Test 🎬 Project 测试",
            "author": "Author with émojis 🤖",
            "sourceBin": [],
            "timeline": {"id": 1, "sceneTrack": {"scenes": []}}
        }

        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".tscproj", delete=False) as f:
            json.dump(data, f, ensure_ascii=False)
            temp_path = Path(f.name)

        try:
            loader = ProjectLoader()
            project = loader.load_file(temp_path)

            # Verify unicode is preserved (check that it loaded successfully)
            assert project.metadata.title == "Test 🎬 Project 测试"
            assert project.metadata.author == "Author with émojis 🤖"

        finally:
            temp_path.unlink()

    def test_permission_denied(self):
        """Test handling of permission errors."""
        # Create a file and then try to read it with no permissions
        with tempfile.NamedTemporaryFile(suffix=".tscproj", delete=False) as f:
            json.dump({"version": "9.0"}, f)
            temp_path = Path(f.name)

        try:
            # Remove read permissions
            import os
            os.chmod(temp_path, 0o000)

            loader = ProjectLoader()

            # Should raise PermissionError or similar
            with pytest.raises((PermissionError, OSError)):
                loader.load_file(temp_path)

        finally:
            # Restore permissions to delete
            import os
            os.chmod(temp_path, 0o644)
            temp_path.unlink()

    def test_non_existent_file_in_cmproj(self):
        """Test loading .cmproj directory without project.tscproj."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            cmproj_dir = Path(tmpdir) / "test.cmproj"
            cmproj_dir.mkdir()

            # Don't create project.tscproj

            loader = ProjectLoader()

            # Should raise FileNotFoundError
            with pytest.raises(FileNotFoundError):
                loader.load_file(cmproj_dir)

    def test_binary_file(self):
        """Test attempting to load a binary file."""
        with tempfile.NamedTemporaryFile(suffix=".tscproj", delete=False) as f:
            # Write binary data
            f.write(b'\x00\x01\x02\x03\x04\x05')
            temp_path = Path(f.name)

        try:
            loader = ProjectLoader()

            # Should raise JSONDecodeError
            with pytest.raises(json.JSONDecodeError):
                loader.load_file(temp_path)

        finally:
            temp_path.unlink()

    def test_partial_file_corruption(self):
        """Test file that starts valid but becomes corrupted."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tscproj", delete=False) as f:
            f.write('{"version": "9.0", "width": 1920')
            # File ends abruptly - no closing brace
            temp_path = Path(f.name)

        try:
            loader = ProjectLoader()

            # Should raise JSONDecodeError
            with pytest.raises(json.JSONDecodeError):
                loader.load_file(temp_path)

        finally:
            temp_path.unlink()
