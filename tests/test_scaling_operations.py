# this_file: tests/test_scaling_operations.py
"""Comprehensive tests for spatial and temporal scaling operations."""

import tempfile
from pathlib import Path

import pytest

from camtasio.models import Project
from camtasio.serialization import ProjectLoader, ProjectSaver
from camtasio.transforms import PropertyTransformer, TransformConfig, TransformType


class TestSpatialScaling:
    """Test spatial (X/Y) scaling operations."""

    def test_scale_factors(self):
        """Test various scale factors."""
        project = Project.empty(width=1920, height=1080)

        # Test different scale factors
        test_cases = [
            (0.5, 960, 540),    # Scale down
            (1.0, 1920, 1080),  # No change
            (2.0, 3840, 2160),  # Scale up
            (1.5, 2880, 1620),  # Fractional scale
        ]

        for factor, expected_width, expected_height in test_cases:
            config = TransformConfig(TransformType.SPATIAL, factor=factor)
            transformer = PropertyTransformer(config)
            scaled = transformer.transform_project(project)

            assert scaled.canvas.width == expected_width
            assert scaled.canvas.height == expected_height

    def test_invalid_scale_factors(self):
        """Test invalid scale factors."""
        project = Project.empty()

        # Test negative scale factor
        config = TransformConfig(TransformType.SPATIAL, factor=-1.0)
        transformer = PropertyTransformer(config)

        with pytest.raises(ValueError, match="Scale factor must be positive"):
            transformer.transform_project(project)

        # Test zero scale factor
        config = TransformConfig(TransformType.SPATIAL, factor=0.0)
        transformer = PropertyTransformer(config)

        with pytest.raises(ValueError, match="Scale factor must be positive"):
            transformer.transform_project(project)

    def test_extreme_scale_factors(self):
        """Test extreme scale factors."""
        project = Project.empty(width=1920, height=1080)

        # Very small scale
        config = TransformConfig(TransformType.SPATIAL, factor=0.01)
        transformer = PropertyTransformer(config)
        scaled = transformer.transform_project(project)

        assert scaled.canvas.width == 19
        assert scaled.canvas.height == 11  # 1080 * 0.01 = 10.8, rounds to 11

        # Very large scale
        config = TransformConfig(TransformType.SPATIAL, factor=10.0)
        transformer = PropertyTransformer(config)
        scaled = transformer.transform_project(project)

        assert scaled.canvas.width == 19200
        assert scaled.canvas.height == 10800

    def test_aspect_ratio_preservation(self):
        """Test that aspect ratio is preserved during scaling."""
        # Test various aspect ratios
        test_cases = [
            (1920, 1080),  # 16:9
            (1280, 720),   # 16:9
            (1920, 1200),  # 16:10
            (1024, 768),   # 4:3
            (2560, 1080),  # 21:9 ultrawide
        ]

        for width, height in test_cases:
            project = Project.empty(width=width, height=height)
            original_ratio = width / height

            config = TransformConfig(TransformType.SPATIAL, factor=1.5)
            transformer = PropertyTransformer(config)
            scaled = transformer.transform_project(project)

            scaled_ratio = scaled.canvas.width / scaled.canvas.height
            assert abs(original_ratio - scaled_ratio) < 0.001  # Allow small rounding error

    def test_media_position_scaling(self):
        """Test that media positions are scaled correctly."""
        project_data = {
            "version": "9.0",
            "editRate": 705600000,
            "width": 1920,
            "height": 1080,
            "videoFormatFrameRate": 30,
            "sourceBin": [],
            "timeline": {
                "id": 1,
                "sceneTrack": {
                    "scenes": [{
                        "csml": {
                            "tracks": [{
                                "medias": [{
                                    "_type": "VMFile",
                                    "parameters": {
                                        "translation0": 100,
                                        "translation1": 200,
                                        "scale0": 1.0,
                                        "scale1": 1.0,
                                    }
                                }]
                            }]
                        }
                    }]
                }
            }
        }

        config = TransformConfig(TransformType.SPATIAL, factor=2.0)
        transformer = PropertyTransformer(config)
        scaled = transformer.transform_dict(project_data)

        media_params = scaled["timeline"]["sceneTrack"]["scenes"][0]["csml"]["tracks"][0]["medias"][0]["parameters"]
        assert media_params["translation0"] == 200
        assert media_params["translation1"] == 400
        assert media_params["scale0"] == 2.0  # Scale values are also scaled
        assert media_params["scale1"] == 2.0

    def test_source_bin_scaling(self):
        """Test that source bin dimensions are scaled."""
        project_data = {
            "version": "9.0",
            "editRate": 705600000,
            "width": 1920,
            "height": 1080,
            "videoFormatFrameRate": 30,
            "sourceBin": [{
                "rect": [0, 0, 1920, 1080],
                "sourceTracks": [{
                    "trackRect": [0, 0, 1920, 1080],
                    "range": [0, 100, 0, 50]
                }]
            }],
            "timeline": {"id": 1, "sceneTrack": {"scenes": []}}
        }

        config = TransformConfig(TransformType.SPATIAL, factor=2.0)
        transformer = PropertyTransformer(config)
        scaled = transformer.transform_dict(project_data)

        # Check source bin scaling
        source = scaled["sourceBin"][0]
        assert source["rect"] == [0, 0, 3840, 2160]
        assert source["sourceTracks"][0]["trackRect"] == [0, 0, 3840, 2160]
        # Range values should not be scaled (they're time-based)
        assert source["sourceTracks"][0]["range"] == [0, 100, 0, 50]


class TestTemporalScaling:
    """Test temporal (time) scaling operations."""

    def test_time_scaling_factors(self):
        """Test various time scale factors."""
        project_data = {
            "version": "9.0",
            "editRate": 705600000,
            "width": 1920,
            "height": 1080,
            "videoFormatFrameRate": 30,
            "sourceBin": [],
            "timeline": {
                "id": 1,
                "sceneTrack": {
                    "scenes": [{
                        "csml": {
                            "tracks": [{
                                "medias": [{
                                    "_type": "VMFile",
                                    "start": 100,
                                    "duration": 200,
                                    "markIn": 50,
                                    "markOut": 250
                                }]
                            }]
                        }
                    }]
                }
            }
        }

        test_cases = [
            (0.5, 50, 100, 25, 125),    # Speed up (half time)
            (1.0, 100, 200, 50, 250),   # No change
            (2.0, 200, 400, 100, 500),  # Slow down (double time)
        ]

        for factor, exp_start, exp_dur, exp_in, exp_out in test_cases:
            config = TransformConfig(TransformType.TEMPORAL, factor=factor)
            transformer = PropertyTransformer(config)
            scaled = transformer.transform_dict(project_data.copy())

            media = scaled["timeline"]["sceneTrack"]["scenes"][0]["csml"]["tracks"][0]["medias"][0]
            assert media["start"] == exp_start
            assert media["duration"] == exp_dur
            assert media["markIn"] == exp_in
            assert media["markOut"] == exp_out

    def test_audio_duration_preservation(self):
        """Test that audio duration can be preserved during temporal scaling."""
        project_data = {
            "version": "9.0",
            "editRate": 705600000,
            "width": 1920,
            "height": 1080,
            "videoFormatFrameRate": 30,
            "sourceBin": [],
            "timeline": {
                "id": 1,
                "sceneTrack": {
                    "scenes": [{
                        "csml": {
                            "tracks": [{
                                "medias": [
                                    {
                                        "_type": "VMFile",
                                        "start": 100,
                                        "duration": 200
                                    },
                                    {
                                        "_type": "AMFile",
                                        "start": 300,
                                        "duration": 100
                                    }
                                ]
                            }]
                        }
                    }]
                }
            }
        }

        # Test with preservation enabled (default)
        config = TransformConfig(TransformType.TEMPORAL, factor=2.0, preserve_audio_duration=True)
        transformer = PropertyTransformer(config)
        scaled = transformer.transform_dict(project_data.copy())

        medias = scaled["timeline"]["sceneTrack"]["scenes"][0]["csml"]["tracks"][0]["medias"]

        # Video scaled
        assert medias[0]["start"] == 200
        assert medias[0]["duration"] == 400

        # Audio position scaled but duration preserved
        assert medias[1]["start"] == 600
        assert medias[1]["duration"] == 100  # Preserved!

        # Test with preservation disabled
        config = TransformConfig(TransformType.TEMPORAL, factor=2.0, preserve_audio_duration=False)
        transformer = PropertyTransformer(config)
        scaled = transformer.transform_dict(project_data.copy())

        medias = scaled["timeline"]["sceneTrack"]["scenes"][0]["csml"]["tracks"][0]["medias"]

        # Both scaled
        assert medias[0]["duration"] == 400
        assert medias[1]["duration"] == 200  # Also scaled

    def test_keyframe_time_scaling(self):
        """Test that keyframe times are scaled correctly."""
        project_data = {
            "version": "9.0",
            "editRate": 705600000,
            "width": 1920,
            "height": 1080,
            "videoFormatFrameRate": 30,
            "sourceBin": [],
            "timeline": {
                "id": 1,
                "sceneTrack": {
                    "scenes": [{
                        "csml": {
                            "tracks": [{
                                "medias": [{
                                    "_type": "VMFile",
                                    "parameters": {
                                        "opacity": {
                                            "keyframes": [
                                                {"time": 0, "value": 0.0},
                                                {"time": 100, "value": 1.0},
                                                {"time": 200, "value": 0.5}
                                            ]
                                        }
                                    }
                                }]
                            }]
                        }
                    }]
                }
            }
        }

        config = TransformConfig(TransformType.TEMPORAL, factor=2.0)
        transformer = PropertyTransformer(config)
        scaled = transformer.transform_dict(project_data)

        keyframes = scaled["timeline"]["sceneTrack"]["scenes"][0]["csml"]["tracks"][0]["medias"][0]["parameters"]["opacity"]["keyframes"]

        # Times scaled, values unchanged
        assert keyframes[0]["time"] == 0
        assert keyframes[0]["value"] == 0.0
        assert keyframes[1]["time"] == 200
        assert keyframes[1]["value"] == 1.0
        assert keyframes[2]["time"] == 400
        assert keyframes[2]["value"] == 0.5

    def test_edit_rate_consistency(self):
        """Test that edit rate is not changed during scaling."""
        for edit_rate in [60, 30, 705600000]:
            project_data = {
                "version": "9.0",
                "editRate": edit_rate,
                "width": 1920,
                "height": 1080,
                "videoFormatFrameRate": 30,
                "sourceBin": [],
                "timeline": {"id": 1, "sceneTrack": {"scenes": []}}
            }

            # Test spatial scaling
            config = TransformConfig(TransformType.SPATIAL, factor=2.0)
            transformer = PropertyTransformer(config)
            scaled = transformer.transform_dict(project_data.copy())
            assert scaled["editRate"] == edit_rate

            # Test temporal scaling
            config = TransformConfig(TransformType.TEMPORAL, factor=2.0)
            transformer = PropertyTransformer(config)
            scaled = transformer.transform_dict(project_data.copy())
            assert scaled["editRate"] == edit_rate


class TestScalingIntegration:
    """Test integration of scaling operations with the full pipeline."""

    def test_load_scale_save_round_trip(self):
        """Test loading, scaling, and saving a project."""
        # Create a test project
        project = Project.empty(width=1920, height=1080)

        with tempfile.NamedTemporaryFile(suffix=".tscproj", delete=False) as f:
            temp_path = Path(f.name)

        try:
            # Save original
            saver = ProjectSaver()
            saver.save_file(project, temp_path)

            # Load
            loader = ProjectLoader()
            loaded = loader.load_file(temp_path)

            # Scale
            config = TransformConfig(TransformType.SPATIAL, factor=2.0)
            transformer = PropertyTransformer(config)
            scaled = transformer.transform_project(loaded)

            # Save scaled
            saver.save_file(scaled, temp_path)

            # Load again
            reloaded = loader.load_file(temp_path)

            # Verify scaling was preserved
            assert reloaded.canvas.width == 3840
            assert reloaded.canvas.height == 2160

        finally:
            temp_path.unlink()

    def test_combined_spatial_and_temporal_scaling(self):
        """Test applying both spatial and temporal scaling."""
        project_data = {
            "version": "9.0",
            "editRate": 705600000,
            "width": 1920,
            "height": 1080,
            "videoFormatFrameRate": 30,
            "sourceBin": [{
                "rect": [0, 0, 1920, 1080]
            }],
            "timeline": {
                "id": 1,
                "sceneTrack": {
                    "scenes": [{
                        "csml": {
                            "tracks": [{
                                "medias": [{
                                    "_type": "VMFile",
                                    "start": 100,
                                    "duration": 200,
                                    "parameters": {
                                        "translation0": 100
                                    }
                                }]
                            }]
                        }
                    }]
                }
            }
        }

        # First apply spatial scaling
        spatial_config = TransformConfig(TransformType.SPATIAL, factor=2.0)
        spatial_transformer = PropertyTransformer(spatial_config)
        spatial_scaled = spatial_transformer.transform_dict(project_data.copy())

        # Then apply temporal scaling
        temporal_config = TransformConfig(TransformType.TEMPORAL, factor=1.5)
        temporal_transformer = PropertyTransformer(temporal_config)
        final_scaled = temporal_transformer.transform_dict(spatial_scaled)

        # Verify both transformations applied
        assert final_scaled["width"] == 3840
        assert final_scaled["height"] == 2160
        assert final_scaled["sourceBin"][0]["rect"] == [0, 0, 3840, 2160]

        media = final_scaled["timeline"]["sceneTrack"]["scenes"][0]["csml"]["tracks"][0]["medias"][0]
        assert media["start"] == 150  # 100 * 1.5
        assert media["duration"] == 300  # 200 * 1.5
        assert media["parameters"]["translation0"] == 200  # 100 * 2.0

    def test_scaling_preserves_structure(self):
        """Test that scaling preserves the overall project structure."""
        # Complex project structure
        project_data = {
            "version": "9.0",
            "editRate": 705600000,
            "width": 1920,
            "height": 1080,
            "videoFormatFrameRate": 30,
            "metadata": {
                "title": "Test Project",
                "author": "Test Author"
            },
            "sourceBin": [{
                "id": 1,
                "src": 1,
                "rect": [0, 0, 1920, 1080]
            }],
            "timeline": {
                "id": 1,
                "sceneTrack": {
                    "scenes": [{
                        "duration": 1000,
                        "csml": {
                            "tracks": [
                                {
                                    "trackIndex": 0,
                                    "medias": [{"_type": "VMFile", "id": 1}]
                                },
                                {
                                    "trackIndex": 1,
                                    "medias": [{"_type": "AMFile", "id": 2}]
                                }
                            ]
                        }
                    }]
                }
            }
        }

        config = TransformConfig(TransformType.SPATIAL, factor=2.0)
        transformer = PropertyTransformer(config)
        scaled = transformer.transform_dict(project_data)

        # Verify structure preserved
        assert "metadata" in scaled
        assert scaled["metadata"]["title"] == "Test Project"
        assert scaled["metadata"]["author"] == "Test Author"
        assert len(scaled["timeline"]["sceneTrack"]["scenes"][0]["csml"]["tracks"]) == 2
        assert scaled["timeline"]["sceneTrack"]["scenes"][0]["csml"]["tracks"][0]["trackIndex"] == 0
        assert scaled["timeline"]["sceneTrack"]["scenes"][0]["csml"]["tracks"][1]["trackIndex"] == 1
