# this_file: tests/test_version_compatibility.py
"""Test loading/saving projects with different Camtasia versions."""

import json
import tempfile
from pathlib import Path

import pytest

from camtasio.models import Project
from camtasio.serialization import ProjectLoader, ProjectSaver, ProjectVersion, detect_version


class TestVersionCompatibility:
    """Test compatibility with different Camtasia versions."""

    @pytest.fixture
    def v4_project_data(self):
        """Sample Camtasia 2020 (v4.0) project data."""
        return {
            "version": "4.0",
            "editRate": 60,
            "width": 1920,
            "height": 1080,
            "videoFormatFrameRate": 30,
            "authoringClientName": "Camtasia Windows",
            "authoringClientVersion": "2020.0.12",
            "sourceBin": [],
            "timeline": {
                "id": 1,
                "sceneTrack": {
                    "scenes": [
                        {
                            "duration": 300,
                            "csml": {
                                "tracks": []
                            }
                        }
                    ]
                }
            }
        }

    @pytest.fixture
    def v9_project_data(self):
        """Sample Camtasia 2021+ (v9.0) project data."""
        return {
            "version": "9.0",
            "editRate": 705600000,
            "width": 1920,
            "height": 1080,
            "videoFormatFrameRate": 30,
            "authoringClientName": "Camtasia Windows",
            "authoringClientVersion": "2023.2.0",
            "sourceBin": [],
            "timeline": {
                "id": 1,
                "sceneTrack": {
                    "scenes": [
                        {
                            "duration": 141120000,
                            "csml": {
                                "tracks": []
                            }
                        }
                    ]
                }
            }
        }

    @pytest.fixture
    def legacy_project_data(self):
        """Sample legacy (v1.0) project data."""
        return {
            "version": "1.0",
            "editRate": 30,
            "width": 1280,
            "height": 720,
            "sourceBin": [],
            "timeline": {
                "id": 1,
                "sceneTrack": {
                    "scenes": []
                }
            }
        }

    def test_detect_versions(self, v4_project_data, v9_project_data, legacy_project_data):
        """Test version detection for different project versions."""
        assert detect_version(v4_project_data) == ProjectVersion.V4_0
        assert detect_version(v9_project_data) == ProjectVersion.V9_0
        assert detect_version(legacy_project_data) == ProjectVersion.V1_0
        assert detect_version({}) == ProjectVersion.UNKNOWN

    def test_load_v4_project(self, v4_project_data):
        """Test loading Camtasia 2020 (v4.0) project."""
        loader = ProjectLoader()
        project = loader.load_dict(v4_project_data)

        assert project.metadata.version == "4.0"
        assert project.metadata.edit_rate == 60
        assert project.canvas.width == 1920
        assert project.canvas.height == 1080
        assert project.metadata.authoring_client_name == "Camtasia Windows"

    def test_load_v9_project(self, v9_project_data):
        """Test loading Camtasia 2021+ (v9.0) project."""
        loader = ProjectLoader()
        project = loader.load_dict(v9_project_data)

        assert project.metadata.version == "9.0"
        assert project.metadata.edit_rate == 705600000
        assert project.canvas.width == 1920
        assert project.canvas.height == 1080
        assert project.metadata.authoring_client_name == "Camtasia Windows"

    def test_load_legacy_project_strict(self, legacy_project_data):
        """Test loading legacy project with strict checking."""
        loader = ProjectLoader(strict_version_check=True)

        # Legacy versions should fail with strict checking
        with pytest.raises(ValueError, match="Unsupported project version"):
            loader.load_dict(legacy_project_data)

    def test_load_legacy_project_lenient(self, legacy_project_data):
        """Test loading legacy project with lenient checking."""
        loader = ProjectLoader(strict_version_check=False)

        # Should load without error
        project = loader.load_dict(legacy_project_data)
        assert project.metadata.version == "1.0"
        assert project.canvas.width == 1280

    def test_save_with_version_preservation(self, v4_project_data):
        """Test that saving preserves the original version."""
        loader = ProjectLoader()
        project = loader.load_dict(v4_project_data)

        saver = ProjectSaver()
        saved_data = saver.project_to_dict(project)

        # Version should be preserved
        assert saved_data["version"] == "4.0"
        assert saved_data["editRate"] == 60

    def test_round_trip_v4(self, v4_project_data):
        """Test round-trip loading/saving for v4.0."""
        with tempfile.NamedTemporaryFile(suffix=".tscproj", delete=False) as f:
            temp_path = Path(f.name)

        try:
            # Write original data
            with open(temp_path, "w") as f:
                json.dump(v4_project_data, f)

            # Load
            loader = ProjectLoader()
            project = loader.load_file(temp_path)

            # Save
            saver = ProjectSaver()
            saver.save_file(project, temp_path)

            # Load again
            reloaded = loader.load_file(temp_path)

            # Verify key properties preserved
            assert reloaded.metadata.version == "4.0"
            assert reloaded.metadata.edit_rate == 60
            assert reloaded.canvas.width == 1920

        finally:
            temp_path.unlink()

    def test_round_trip_v9(self, v9_project_data):
        """Test round-trip loading/saving for v9.0."""
        with tempfile.NamedTemporaryFile(suffix=".tscproj", delete=False) as f:
            temp_path = Path(f.name)

        try:
            # Write original data
            with open(temp_path, "w") as f:
                json.dump(v9_project_data, f)

            # Load
            loader = ProjectLoader()
            project = loader.load_file(temp_path)

            # Save
            saver = ProjectSaver()
            saver.save_file(project, temp_path)

            # Load again
            reloaded = loader.load_file(temp_path)

            # Verify key properties preserved
            assert reloaded.metadata.version == "9.0"
            assert reloaded.metadata.edit_rate == 705600000
            assert reloaded.canvas.width == 1920

        finally:
            temp_path.unlink()

    def test_version_feature_flags(self):
        """Test version-specific feature detection."""
        from camtasio.serialization import get_version_features

        # V4.0 features
        v4_features = get_version_features(ProjectVersion.V4_0)
        assert not v4_features["has_high_precision_timing"]
        assert not v4_features["has_loudness_normalization"]

        # V9.0 features
        v9_features = get_version_features(ProjectVersion.V9_0)
        assert v9_features["has_high_precision_timing"]
        assert v9_features["has_loudness_normalization"]
        assert v9_features["has_authoring_client"]

    def test_mixed_version_project_handling(self):
        """Test handling projects with conflicting version information."""
        # Project claims to be v4.0 but has v9.0 edit rate
        mixed_data = {
            "version": "4.0",
            "editRate": 705600000,  # This is v9.0 rate
            "width": 1920,
            "height": 1080,
            "videoFormatFrameRate": 30,
            "sourceBin": [],
            "timeline": {"id": 1, "sceneTrack": {"scenes": [{"csml": {"tracks": []}}]}}
        }

        loader = ProjectLoader()
        project = loader.load_dict(mixed_data)

        # Should respect the stated version but preserve the edit rate
        assert project.metadata.version == "4.0"
        assert project.metadata.edit_rate == 705600000

    def test_minimal_project_different_versions(self):
        """Test creating minimal projects for different versions."""
        # Create empty projects with different target versions
        v4_project = Project.empty()
        v4_project.metadata.version = "4.0"
        v4_project.metadata.edit_rate = 60

        v9_project = Project.empty()
        v9_project.metadata.version = "9.0"
        v9_project.metadata.edit_rate = 705600000

        saver = ProjectSaver()

        # Save and verify v4
        v4_dict = saver.project_to_dict(v4_project)
        assert v4_dict["version"] == "4.0"
        assert v4_dict["editRate"] == 60

        # Save and verify v9
        v9_dict = saver.project_to_dict(v9_project)
        assert v9_dict["version"] == "9.0"
        assert v9_dict["editRate"] == 705600000

    def test_version_migration_warnings(self, v4_project_data):
        """Test that version information is preserved during loading."""
        loader = ProjectLoader()

        # Load v4 project
        project = loader.load_dict(v4_project_data)

        # Check that version is correctly loaded
        assert project.metadata.version == "4.0"
        assert project.metadata.edit_rate == 60

        # Load a project with unknown version
        unknown_data = v4_project_data.copy()
        unknown_data["version"] = "99.0"

        # Should still load with lenient mode
        lenient_loader = ProjectLoader(strict_version_check=False)
        project = lenient_loader.load_dict(unknown_data)
        assert project.metadata.version == "99.0"

    def test_unknown_version_handling(self):
        """Test handling of unknown/future versions."""
        future_data = {
            "version": "15.0",  # Future version
            "editRate": 1000000000,
            "width": 3840,
            "height": 2160,
            "sourceBin": [],
            "timeline": {"id": 1, "sceneTrack": {"scenes": []}}
        }

        # Strict mode should fail
        strict_loader = ProjectLoader(strict_version_check=True)
        with pytest.raises(ValueError, match="Unsupported project version"):
            strict_loader.load_dict(future_data)

        # Lenient mode should load
        lenient_loader = ProjectLoader(strict_version_check=False)
        project = lenient_loader.load_dict(future_data)
        assert project.metadata.version == "15.0"
        assert project.canvas.width == 3840
