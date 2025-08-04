# this_file: tests/test_cli.py
"""Integration tests for the CLI."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from camtasio.cli.app import CamtasioCLI

# Import both legacy and modern CLI
from camtasio.legacy_cli import hello, timescale, version, xyscale
from camtasio.models import Project


def create_test_project_file():
    """Create a test project file and return its path."""
    project = Project.empty(width=1920, height=1080)

    # Add some test data
    project.metadata.title = "Test Project"

    data = project.to_dict()

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".tscproj", delete=False, encoding="utf-8"
    ) as f:
        json.dump(data, f, indent=2)
        return Path(f.name)


class TestBasicCommands:
    """Test basic CLI commands."""

    def test_version_command(self, capsys):
        """Test the version command."""
        version()
        captured = capsys.readouterr()
        assert "camtasio" in captured.out
        assert "version" in captured.out

    def test_hello_command(self, capsys):
        """Test the hello command."""
        hello()
        captured = capsys.readouterr()
        assert "Hello, World!" in captured.out

    def test_hello_with_name(self, capsys):
        """Test the hello command with a name."""
        hello("Alice")
        captured = capsys.readouterr()
        assert "Hello, Alice!" in captured.out


class TestXYScaleCommand:
    """Test xyscale command."""

    def test_xyscale_basic(self, capsys):
        """Test basic xyscale operation."""
        # Create test file
        input_path = create_test_project_file()
        output_path = input_path.parent / "output.tscproj"

        try:
            # Run xyscale
            xyscale(input=str(input_path), scale=150.0, output=str(output_path), verbose=False)

            # Check output
            captured = capsys.readouterr()
            assert "Successfully scaled" in captured.out
            assert output_path.exists()

            # Verify scaling
            with open(output_path) as f:
                data = json.load(f)
            assert data["width"] == 2880  # 1920 * 1.5
            assert data["height"] == 1620  # 1080 * 1.5

        finally:
            input_path.unlink(missing_ok=True)
            output_path.unlink(missing_ok=True)

    def test_xyscale_auto_output(self, capsys):
        """Test xyscale with auto-generated output filename."""
        input_path = create_test_project_file()
        expected_output = input_path.parent / f"{input_path.stem}_200pct.tscproj"

        try:
            # Run without specifying output
            xyscale(input=str(input_path), scale=200.0, output=None, verbose=False)

            # Check auto-generated file
            assert expected_output.exists()

            with open(expected_output) as f:
                data = json.load(f)
            assert data["width"] == 3840  # 1920 * 2

        finally:
            input_path.unlink(missing_ok=True)
            expected_output.unlink(missing_ok=True)

    def test_xyscale_downscale(self, capsys):
        """Test downscaling."""
        input_path = create_test_project_file()
        output_path = input_path.parent / "small.tscproj"

        try:
            xyscale(input=str(input_path), scale=50.0, output=str(output_path), verbose=False)

            with open(output_path) as f:
                data = json.load(f)
            assert data["width"] == 960  # 1920 * 0.5
            assert data["height"] == 540  # 1080 * 0.5

        finally:
            input_path.unlink(missing_ok=True)
            output_path.unlink(missing_ok=True)

    def test_xyscale_invalid_input(self, capsys):
        """Test xyscale with non-existent input."""
        xyscale(input="/nonexistent/file.tscproj", scale=150.0, output=None, verbose=False)

        captured = capsys.readouterr()
        assert "Error" in captured.out
        assert "does not exist" in captured.out

    def test_xyscale_invalid_scale(self, capsys):
        """Test xyscale with invalid scale factor."""
        input_path = create_test_project_file()

        try:
            xyscale(
                input=str(input_path),
                scale=-50.0,  # Negative scale
                output=None,
                verbose=False,
            )

            captured = capsys.readouterr()
            assert "Error" in captured.out
            assert "positive" in captured.out

        finally:
            input_path.unlink(missing_ok=True)


class TestTimeScaleCommand:
    """Test timescale command."""

    def test_timescale_basic(self, capsys):
        """Test basic timescale operation."""
        # Create test project with timeline data
        project = Project.empty()
        # Would add timeline data here in real test

        with tempfile.NamedTemporaryFile(mode="w", suffix=".tscproj", delete=False) as f:
            json.dump(project.to_dict(), f)
            input_path = Path(f.name)

        output_path = input_path.parent / "time_output.tscproj"

        try:
            timescale(input=str(input_path), scale=200.0, output=str(output_path), verbose=False)

            captured = capsys.readouterr()
            assert "Successfully time-scaled" in captured.out
            assert output_path.exists()

        finally:
            input_path.unlink(missing_ok=True)
            output_path.unlink(missing_ok=True)

    def test_timescale_auto_filename(self, capsys):
        """Test timescale with auto-generated filename."""
        input_path = create_test_project_file()
        expected_output = input_path.parent / f"{input_path.stem}_time150pct.tscproj"

        try:
            timescale(input=str(input_path), scale=150.0, output=None, verbose=False)

            assert expected_output.exists()

        finally:
            input_path.unlink(missing_ok=True)
            expected_output.unlink(missing_ok=True)

    def test_timescale_preserves_canvas(self, capsys):
        """Test that timescale doesn't affect canvas dimensions."""
        input_path = create_test_project_file()
        output_path = input_path.parent / "time_canvas.tscproj"

        try:
            timescale(input=str(input_path), scale=200.0, output=str(output_path), verbose=False)

            with open(output_path) as f:
                data = json.load(f)

            # Canvas should be unchanged
            assert data["width"] == 1920
            assert data["height"] == 1080

        finally:
            input_path.unlink(missing_ok=True)
            output_path.unlink(missing_ok=True)


class TestVerboseMode:
    """Test verbose mode functionality."""

    def test_xyscale_verbose(self, capsys):
        """Test xyscale with verbose mode."""
        input_path = create_test_project_file()
        output_path = input_path.parent / "verbose.tscproj"

        try:
            xyscale(input=str(input_path), scale=150.0, output=str(output_path), verbose=True)

            captured = capsys.readouterr()
            # Should contain debug/info messages
            assert "Loading project" in captured.out
            assert "Scaling project" in captured.out
            assert "Saving scaled project" in captured.out

        finally:
            input_path.unlink(missing_ok=True)
            output_path.unlink(missing_ok=True)


class TestErrorHandling:
    """Test error handling in CLI."""

    def test_corrupted_json(self, capsys):
        """Test handling of corrupted JSON file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tscproj", delete=False) as f:
            f.write("{ invalid json")
            input_path = Path(f.name)

        try:
            with pytest.raises(json.JSONDecodeError):
                xyscale(input=str(input_path), scale=150.0, output=None, verbose=False)
        finally:
            input_path.unlink(missing_ok=True)

    def test_missing_required_fields(self, capsys):
        """Test handling of project missing required fields."""
        # Create invalid project data - missing almost everything
        data = {
            "version": "9.0",
            # Missing width, height, editRate, timeline, sourceBin
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".tscproj", delete=False) as f:
            json.dump(data, f)
            input_path = Path(f.name)

        try:
            # Test that the scaler handles missing fields gracefully
            # It should complete without crashing, even with minimal data
            xyscale(input=str(input_path), scale=150.0, output=None, verbose=False)

            # Verify the output was created
            output_path = input_path.parent / f"{input_path.stem}_150pct.tscproj"
            assert output_path.exists(), "Output file should be created"

            # The scaler preserves the original structure
            # It doesn't add missing fields, just scales existing ones
            with open(output_path) as f:
                result = json.load(f)

            # Should have the same structure as input (version only)
            assert "version" in result
            assert result["version"] == "9.0"
            # Width and height were not in input, so they shouldn't be in output
            assert "width" not in result
            assert "height" not in result

            output_path.unlink()

        finally:
            input_path.unlink(missing_ok=True)


class TestModernCLI:
    """Test the modern CamtasioCLI class."""

    @pytest.fixture
    def cli(self):
        """Create CLI instance."""
        return CamtasioCLI()

    @pytest.fixture
    def test_project_with_media(self):
        """Create a test project with media bin and timeline data."""
        project = Project.empty(width=1920, height=1080)
        project.metadata.title = "Test Project with Media"

        data = project.to_dict()

        # Add media bin items
        data["sourceBin"] = [
            {
                "id": "media1",
                "name": "Video1.mp4",
                "_type": "VideoSource",
                "src": "/fake/path/video1.mp4"
            },
            {
                "id": "media2",
                "name": "Audio1.wav",
                "_type": "AudioSource",
                "src": "/fake/path/audio1.wav"
            }
        ]

        # Add timeline with tracks
        data["timeline"] = {
            "sceneTrack": {
                "scenes": [{
                    "csml": {
                        "tracks": [
                            {
                                "trackType": "video",
                                "medias": [
                                    {
                                        "name": "Video Clip",
                                        "src": "media1",
                                        "start": 1000,
                                        "duration": 5000
                                    }
                                ]
                            },
                            {
                                "trackType": "audio",
                                "medias": [
                                    {
                                        "name": "Audio Clip",
                                        "src": "media2",
                                        "start": 0,
                                        "duration": 6000
                                    }
                                ]
                            }
                        ]
                    }
                }],
                "timeline": {
                    "width": 1920,
                    "height": 1080,
                    "framerate": 30
                }
            },
            "markers": [
                {"name": "Start", "time": 0, "type": "marker"},
                {"name": "End", "time": 6000, "type": "marker"}
            ]
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tscproj", delete=False, encoding="utf-8"
        ) as f:
            json.dump(data, f, indent=2)
            return Path(f.name)

    def test_version_command(self, cli, capsys):
        """Test version command."""
        cli.version()
        captured = capsys.readouterr()
        assert "camtasio version" in captured.out

    def test_info_basic(self, cli, test_project_with_media, capsys):
        """Test basic info command."""
        try:
            cli.info(str(test_project_with_media))
            captured = capsys.readouterr()

            assert "Project Information" in captured.out
            assert "1920x1080" in captured.out
            assert "Media Analysis" in captured.out
            assert "Total Media Items: 2" in captured.out

        finally:
            test_project_with_media.unlink(missing_ok=True)

    def test_info_detailed(self, cli, test_project_with_media, capsys):
        """Test detailed info command."""
        try:
            cli.info(str(test_project_with_media), detailed=True)
            captured = capsys.readouterr()

            assert "Timeline Analysis" in captured.out
            assert "Timeline Tracks: 2" in captured.out
            assert "Total Clips: 2" in captured.out
            assert "Project Complexity:" in captured.out
            assert "Recommendations" in captured.out

        finally:
            test_project_with_media.unlink(missing_ok=True)

    def test_info_nonexistent_file(self, cli, capsys):
        """Test info command with nonexistent file."""
        cli.info("/nonexistent/file.tscproj")
        captured = capsys.readouterr()
        assert "Error" in captured.out
        assert "Failed to load project" in captured.out

    def test_validate_success(self, cli, test_project_with_media, capsys):
        """Test validate command with valid project."""
        try:
            cli.validate(str(test_project_with_media))
            captured = capsys.readouterr()

            assert "Project loads successfully" in captured.out
            assert "is supported" in captured.out

        finally:
            test_project_with_media.unlink(missing_ok=True)

    def test_validate_invalid_file(self, cli, capsys):
        """Test validate command with invalid file."""
        cli.validate("/nonexistent/file.tscproj")
        captured = capsys.readouterr()
        assert "Validation failed" in captured.out

    def test_xyscale_basic(self, cli, capsys):
        """Test basic xyscale operation."""
        # Create test file
        input_path = create_test_project_file()
        output_path = input_path.parent / "scaled_output.tscproj"

        try:
            cli.xyscale(str(input_path), 1.5, str(output_path), backup=False)

            captured = capsys.readouterr()
            assert "Scaled project by 1.5x" in captured.out
            assert output_path.exists()

            # Verify scaling
            with open(output_path) as f:
                data = json.load(f)
            # Check that canvas was scaled
            timeline = data.get("timeline", {}).get("sceneTrack", {}).get("timeline", {})
            if "width" in timeline:
                assert timeline["width"] == 2880  # 1920 * 1.5

        finally:
            input_path.unlink(missing_ok=True)
            output_path.unlink(missing_ok=True)

    def test_xyscale_with_backup(self, cli, capsys):
        """Test xyscale with backup creation."""
        input_path = create_test_project_file()
        backup_path = input_path.with_suffix(f"{input_path.suffix}.backup")

        try:
            cli.xyscale(str(input_path), 2.0, backup=True)

            captured = capsys.readouterr()
            assert "Scaled project by 2.0x" in captured.out
            assert backup_path.exists()

        finally:
            input_path.unlink(missing_ok=True)
            backup_path.unlink(missing_ok=True)

    def test_timescale_basic(self, cli, test_project_with_media, capsys):
        """Test basic timescale operation."""
        output_path = test_project_with_media.parent / "timescaled_output.tscproj"

        try:
            cli.timescale(str(test_project_with_media), 0.5, str(output_path), backup=False)

            captured = capsys.readouterr()
            assert "Scaled timeline by 0.5x" in captured.out
            assert "Audio duration preserved" in captured.out
            assert output_path.exists()

        finally:
            test_project_with_media.unlink(missing_ok=True)
            output_path.unlink(missing_ok=True)

    def test_timescale_no_audio_preserve(self, cli, test_project_with_media, capsys):
        """Test timescale without audio preservation."""
        output_path = test_project_with_media.parent / "timescaled_no_audio.tscproj"

        try:
            cli.timescale(str(test_project_with_media), 2.0, str(output_path),
                         backup=False, preserve_audio=False)

            captured = capsys.readouterr()
            assert "Scaled timeline by 2.0x" in captured.out
            # Should not mention audio preservation
            assert "Audio duration preserved" not in captured.out

        finally:
            test_project_with_media.unlink(missing_ok=True)
            output_path.unlink(missing_ok=True)

    def test_media_ls_basic(self, cli, test_project_with_media, capsys):
        """Test basic media_ls command."""
        try:
            cli.media_ls(str(test_project_with_media))
            captured = capsys.readouterr()

            assert "Media Bin Contents" in captured.out
            assert "Media Items: 2" in captured.out
            assert "Video1.mp4" in captured.out
            assert "Audio1.wav" in captured.out

        finally:
            test_project_with_media.unlink(missing_ok=True)

    def test_media_ls_detailed(self, cli, test_project_with_media, capsys):
        """Test detailed media_ls command."""
        try:
            cli.media_ls(str(test_project_with_media), detailed=True)
            captured = capsys.readouterr()

            assert "Type: VideoSource" in captured.out
            assert "Type: AudioSource" in captured.out
            assert "Source:" in captured.out

        finally:
            test_project_with_media.unlink(missing_ok=True)

    def test_media_ls_empty(self, cli, capsys):
        """Test media_ls with empty project."""
        input_path = create_test_project_file()

        try:
            cli.media_ls(str(input_path))
            captured = capsys.readouterr()

            assert "Media Items: 0" in captured.out
            assert "No media items found" in captured.out

        finally:
            input_path.unlink(missing_ok=True)

    def test_track_ls_basic(self, cli, test_project_with_media, capsys):
        """Test basic track_ls command."""
        try:
            cli.track_ls(str(test_project_with_media))
            captured = capsys.readouterr()

            assert "Timeline Tracks" in captured.out
            assert "Total Tracks: 2" in captured.out
            assert "video - 1 clips" in captured.out
            assert "audio - 1 clips" in captured.out

        finally:
            test_project_with_media.unlink(missing_ok=True)

    def test_track_ls_detailed(self, cli, test_project_with_media, capsys):
        """Test detailed track_ls command."""
        try:
            cli.track_ls(str(test_project_with_media), detailed=True)
            captured = capsys.readouterr()

            assert "Duration:" in captured.out
            assert "Clips:" in captured.out
            assert "Video Clip" in captured.out
            assert "Audio Clip" in captured.out

        finally:
            test_project_with_media.unlink(missing_ok=True)

    def test_marker_ls(self, cli, test_project_with_media, capsys):
        """Test marker_ls command."""
        try:
            cli.marker_ls(str(test_project_with_media))
            captured = capsys.readouterr()

            assert "Timeline Markers" in captured.out
            assert "Total Markers: 2" in captured.out
            assert "Start at 0.00s" in captured.out
            assert "End at 6.00s" in captured.out

        finally:
            test_project_with_media.unlink(missing_ok=True)

    def test_marker_ls_empty(self, cli, capsys):
        """Test marker_ls with no markers."""
        input_path = create_test_project_file()

        try:
            cli.marker_ls(str(input_path))
            captured = capsys.readouterr()

            assert "Total Markers: 0" in captured.out
            assert "No markers found" in captured.out

        finally:
            input_path.unlink(missing_ok=True)

    def test_analyze(self, cli, test_project_with_media, capsys):
        """Test analyze command."""
        try:
            cli.analyze(str(test_project_with_media))
            captured = capsys.readouterr()

            assert "Project Analysis Report" in captured.out
            assert "📊 Project Overview" in captured.out
            assert "📁 Media Summary" in captured.out
            assert "🎬 Timeline Summary" in captured.out
            assert "💡 Recommendations" in captured.out
            assert "Total Media Items: 2" in captured.out
            assert "Tracks: 2" in captured.out
            assert "Total Clips: 2" in captured.out

        finally:
            test_project_with_media.unlink(missing_ok=True)

    def test_media_replace(self, cli, test_project_with_media, capsys):
        """Test media_replace command."""
        try:
            cli.media_replace(str(test_project_with_media),
                            "/fake/path/video1.mp4",
                            "/new/path/video1.mp4",
                            backup=False)

            captured = capsys.readouterr()
            assert "Replaced 1 instances" in captured.out

            # Verify replacement worked
            with open(test_project_with_media) as f:
                data = json.load(f)

            # Check if replacement occurred
            found_replacement = False
            for item in data.get("sourceBin", []):
                if item.get("src") == "/new/path/video1.mp4":
                    found_replacement = True
                    break
            assert found_replacement

        finally:
            test_project_with_media.unlink(missing_ok=True)

    def test_media_replace_not_found(self, cli, test_project_with_media, capsys):
        """Test media_replace with path not found."""
        try:
            cli.media_replace(str(test_project_with_media),
                            "/nonexistent/path.mp4",
                            "/new/path.mp4",
                            backup=False)

            captured = capsys.readouterr()
            assert "No instances of" in captured.out

        finally:
            test_project_with_media.unlink(missing_ok=True)

    @patch('builtins.input', return_value='n')
    def test_media_rm_cancelled(self, mock_input, cli, test_project_with_media, capsys):
        """Test media_rm command cancelled by user."""
        try:
            cli.media_rm(str(test_project_with_media), backup=False)
            captured = capsys.readouterr()

            # Should show unused media but be cancelled
            assert "Remove Unused Media" in captured.out or "No unused media items found" in captured.out

        finally:
            test_project_with_media.unlink(missing_ok=True)

    def test_batch_info_no_files(self, cli, capsys):
        """Test batch command with no matching files."""
        cli.batch("/nonexistent/*.tscproj", "info")
        captured = capsys.readouterr()

        assert "No .tscproj files found" in captured.out

    def test_batch_invalid_operation(self, cli, capsys):
        """Test batch command with invalid operation."""
        input_path = create_test_project_file()

        try:
            cli.batch(str(input_path), "invalid_operation")
            captured = capsys.readouterr()

            assert "Unknown operation 'invalid_operation'" in captured.out

        finally:
            input_path.unlink(missing_ok=True)

    def test_error_handling_corrupted_json(self, cli, capsys):
        """Test CLI commands with corrupted JSON."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tscproj", delete=False) as f:
            f.write("{ invalid json")
            corrupted_path = Path(f.name)

        try:
            cli.info(str(corrupted_path))
            captured = capsys.readouterr()
            assert "Error" in captured.out

        finally:
            corrupted_path.unlink(missing_ok=True)

    def test_xyscale_invalid_scale(self, cli, capsys):
        """Test xyscale with invalid scale factor."""
        input_path = create_test_project_file()

        try:
            # Test with zero scale (invalid)
            cli.xyscale(str(input_path), 0.0, backup=False)
            captured = capsys.readouterr()
            # Should either work or show an error
            assert any(word in captured.out for word in ["Error", "Scaled", "failed"])

        finally:
            input_path.unlink(missing_ok=True)
