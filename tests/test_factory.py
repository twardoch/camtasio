# this_file: tests/test_factory.py
"""Tests for factory functions."""


from camtasio.models.factory import create_media_from_dict, detect_media_type
from camtasio.models.media import AudioMedia, Callout, ImageMedia, VideoMedia


class TestCreateMediaFromDict:
    """Test create_media_from_dict function."""

    def test_create_video_media_vmfile(self):
        """Test creating VideoMedia from VMFile type."""
        data = {
            "_type": "VMFile",
            "id": 1,
            "src": 2,
            "trackNumber": 0,
            "start": 1000,
            "duration": 5000,
            "mediaStart": 0,
            "mediaDuration": 5000,
            "scalar": 1.0,
            "attributes": {"visible": True},
            "parameters": {"opacity": 1.0},
            "effects": [],
            "metadata": {"filename": "video.mp4"},
            "animationTracks": {}
        }

        media = create_media_from_dict(data)

        assert isinstance(media, VideoMedia)
        assert media.id == 1
        assert media.src == 2
        assert media.track_number == 0
        assert media.start == 1000
        assert media.duration == 5000
        assert media.scalar == 1.0

    def test_create_video_media_screen_recording(self):
        """Test creating VideoMedia from ScreenVMFile type."""
        data = {
            "_type": "ScreenVMFile",
            "id": 2,
            "src": 3,
            "start": 2000,
            "duration": 3000
        }

        media = create_media_from_dict(data)

        assert isinstance(media, VideoMedia)
        assert media.id == 2
        assert media.src == 3
        assert media.start == 2000
        assert media.duration == 3000

    def test_create_audio_media(self):
        """Test creating AudioMedia from AMFile type."""
        data = {
            "_type": "AMFile",
            "id": 3,
            "src": 4,
            "channelNumber": "0,1",
            "start": 500,
            "duration": 4000
        }

        media = create_media_from_dict(data)

        assert isinstance(media, AudioMedia)
        assert media.id == 3
        assert media.src == 4
        assert media.channel_number == "0,1"
        assert media.start == 500
        assert media.duration == 4000

    def test_create_audio_media_default_channel(self):
        """Test creating AudioMedia with default channel number."""
        data = {
            "_type": "AMFile",
            "id": 4,
            "src": 5
        }

        media = create_media_from_dict(data)

        assert isinstance(media, AudioMedia)
        assert media.channel_number == "0,1"  # Default value

    def test_create_image_media(self):
        """Test creating ImageMedia from IMFile type."""
        data = {
            "_type": "IMFile",
            "id": 5,
            "src": 6,
            "trimStartSum": 100,
            "duration": 2000
        }

        media = create_media_from_dict(data)

        assert isinstance(media, ImageMedia)
        assert media.id == 5
        assert media.src == 6
        assert media.trim_start_sum == 100
        assert media.duration == 2000

    def test_create_image_media_default_trim(self):
        """Test creating ImageMedia with default trim start sum."""
        data = {
            "_type": "IMFile",
            "id": 6,
            "src": 7
        }

        media = create_media_from_dict(data)

        assert isinstance(media, ImageMedia)
        assert media.trim_start_sum == 0  # Default value

    def test_create_callout(self):
        """Test creating Callout media."""
        data = {
            "_type": "Callout",
            "id": 7,
            "src": 8,
            "def": {
                "type": "text",
                "content": "Hello World"
            },
            "duration": 3000
        }

        media = create_media_from_dict(data)

        assert isinstance(media, Callout)
        assert media.id == 7
        assert media.src == 8
        assert media.definition == {"type": "text", "content": "Hello World"}
        assert media.duration == 3000

    def test_create_unified_media(self):
        """Test creating VideoMedia from UnifiedMedia type."""
        data = {
            "_type": "UnifiedMedia",
            "id": 8,
            "src": 9,
            "duration": 6000
        }

        media = create_media_from_dict(data)

        assert isinstance(media, VideoMedia)
        assert media.id == 8
        assert media.src == 9
        assert media.duration == 6000

    def test_create_group_media(self):
        """Test creating VideoMedia from Group type."""
        data = {
            "_type": "Group",
            "id": 9,
            "src": 10,
            "duration": 7000
        }

        media = create_media_from_dict(data)

        assert isinstance(media, VideoMedia)
        assert media.id == 9
        assert media.src == 10
        assert media.duration == 7000

    def test_create_stitched_media(self):
        """Test creating VideoMedia from StitchedMedia type."""
        data = {
            "_type": "StitchedMedia",
            "id": 10,
            "src": 11,
            "duration": 8000
        }

        media = create_media_from_dict(data)

        assert isinstance(media, VideoMedia)
        assert media.id == 10
        assert media.src == 11
        assert media.duration == 8000

    def test_create_unknown_media_type(self):
        """Test creating VideoMedia from unknown type (default)."""
        data = {
            "_type": "UnknownType",
            "id": 11,
            "src": 12,
            "duration": 1000
        }

        media = create_media_from_dict(data)

        # Should default to VideoMedia and log warning
        assert isinstance(media, VideoMedia)
        assert media.id == 11
        assert media.src == 12
        assert media.duration == 1000

    def test_create_media_missing_type(self):
        """Test creating VideoMedia when _type is missing."""
        data = {
            "id": 12,
            "src": 13,
            "duration": 1500
        }

        media = create_media_from_dict(data)

        # Should default to VideoMedia
        assert isinstance(media, VideoMedia)
        assert media.id == 12
        assert media.src == 13
        assert media.duration == 1500

    def test_create_media_with_default_values(self):
        """Test creating media with minimal data (default values)."""
        data = {
            "_type": "VMFile"
        }

        media = create_media_from_dict(data)

        assert isinstance(media, VideoMedia)
        assert media.id == 0  # Default
        assert media.src == 0  # Default
        assert media.track_number == 0  # Default
        assert media.start == 0  # Default
        assert media.duration == 0  # Default
        assert media.media_start == 0  # Default
        assert media.media_duration == 0  # Default
        assert media.scalar == 1.0  # Default
        assert media.attributes == {}  # Default
        assert media.parameters == {}  # Default
        assert media.effects == []  # Default
        assert media.metadata == {}  # Default
        assert media.animation_tracks == {}  # Default

    def test_create_media_with_complex_attributes(self):
        """Test creating media with complex attributes and effects."""
        data = {
            "_type": "VMFile",
            "id": 13,
            "attributes": {
                "visible": True,
                "locked": False,
                "color": "#FF0000"
            },
            "parameters": {
                "opacity": 0.8,
                "volume": 0.5,
                "scale": 1.2
            },
            "effects": [
                {"type": "blur", "intensity": 0.5},
                {"type": "sharpen", "amount": 0.3}
            ],
            "metadata": {
                "filename": "complex_video.mp4",
                "resolution": "1920x1080",
                "framerate": 30
            },
            "animationTracks": {
                "position": [{"time": 0, "x": 100, "y": 200}],
                "scale": [{"time": 1000, "value": 1.5}]
            }
        }

        media = create_media_from_dict(data)

        assert isinstance(media, VideoMedia)
        assert media.id == 13
        assert media.attributes["visible"] is True
        assert media.attributes["color"] == "#FF0000"
        assert media.parameters["opacity"] == 0.8
        assert media.parameters["scale"] == 1.2
        assert len(media.effects) == 2
        assert media.effects[0]["type"] == "blur"
        assert media.metadata["filename"] == "complex_video.mp4"
        assert "position" in media.animation_tracks
        assert "scale" in media.animation_tracks


class TestDetectMediaType:
    """Test detect_media_type function."""

    def test_detect_video_media(self):
        """Test detecting video media type."""
        source_item = {
            "sourceTracks": [
                {"type": 0},  # Video track
                {"type": 2}   # Audio track
            ]
        }

        media_type = detect_media_type(source_item)
        assert media_type == "VMFile"

    def test_detect_screen_recording(self):
        """Test detecting screen recording video type."""
        source_item = {
            "sourceTracks": [
                {"type": 0},  # Video track
                {"type": 2}   # Audio track
            ],
            "metadata": {
                "IsScreenRecording": True
            }
        }

        media_type = detect_media_type(source_item)
        assert media_type == "ScreenVMFile"

    def test_detect_screen_recording_false(self):
        """Test detecting regular video when screen recording is explicitly false."""
        source_item = {
            "sourceTracks": [
                {"type": 0}  # Video track
            ],
            "metadata": {
                "IsScreenRecording": False
            }
        }

        media_type = detect_media_type(source_item)
        assert media_type == "VMFile"

    def test_detect_image_media(self):
        """Test detecting image media type."""
        source_item = {
            "sourceTracks": [
                {"type": 1}  # Image track
            ]
        }

        media_type = detect_media_type(source_item)
        assert media_type == "IMFile"

    def test_detect_audio_media(self):
        """Test detecting audio media type."""
        source_item = {
            "sourceTracks": [
                {"type": 2}  # Audio track
            ]
        }

        media_type = detect_media_type(source_item)
        assert media_type == "AMFile"

    def test_detect_mixed_media_prioritizes_video(self):
        """Test that video is prioritized over other types when multiple tracks exist."""
        source_item = {
            "sourceTracks": [
                {"type": 1},  # Image track
                {"type": 0},  # Video track (should win)
                {"type": 2}   # Audio track
            ]
        }

        media_type = detect_media_type(source_item)
        assert media_type == "VMFile"

    def test_detect_image_and_audio_prioritizes_image(self):
        """Test that image is prioritized over audio when both exist but no video."""
        source_item = {
            "sourceTracks": [
                {"type": 2},  # Audio track
                {"type": 1}   # Image track (should win)
            ]
        }

        media_type = detect_media_type(source_item)
        assert media_type == "IMFile"

    def test_detect_unknown_track_types(self):
        """Test detecting media with unknown track types."""
        source_item = {
            "sourceTracks": [
                {"type": 99},  # Unknown track type
                {"type": 42}   # Another unknown type
            ]
        }

        media_type = detect_media_type(source_item)
        assert media_type == "VMFile"  # Default to video

    def test_detect_empty_source_tracks(self):
        """Test detecting media with empty source tracks."""
        source_item = {
            "sourceTracks": []
        }

        media_type = detect_media_type(source_item)
        assert media_type == "VMFile"  # Default to video

    def test_detect_missing_source_tracks(self):
        """Test detecting media with missing sourceTracks field."""
        source_item = {}

        media_type = detect_media_type(source_item)
        assert media_type == "VMFile"  # Default to video

    def test_detect_tracks_without_type(self):
        """Test detecting media with tracks missing type field."""
        source_item = {
            "sourceTracks": [
                {"name": "track1"},  # Missing type field
                {"duration": 5000}   # Missing type field
            ]
        }

        media_type = detect_media_type(source_item)
        assert media_type == "VMFile"  # Default to video

    def test_detect_tracks_with_negative_type(self):
        """Test detecting media with tracks having default -1 type."""
        source_item = {
            "sourceTracks": [
                {"type": -1},  # Default/unspecified type
                {"type": -1}
            ]
        }

        media_type = detect_media_type(source_item)
        assert media_type == "VMFile"  # Default to video

    def test_detect_mixed_valid_and_invalid_types(self):
        """Test detecting media with mix of valid and invalid track types."""
        source_item = {
            "sourceTracks": [
                {"type": -1},  # Invalid/default
                {"type": 2},   # Audio (valid)
                {"type": 99}   # Unknown
            ]
        }

        media_type = detect_media_type(source_item)
        assert media_type == "AMFile"  # Should detect the valid audio track

    def test_detect_with_metadata_but_no_screen_recording(self):
        """Test video detection with metadata but no screen recording flag."""
        source_item = {
            "sourceTracks": [
                {"type": 0}  # Video track
            ],
            "metadata": {
                "filename": "video.mp4",
                "duration": 30000
            }
        }

        media_type = detect_media_type(source_item)
        assert media_type == "VMFile"  # Regular video, not screen recording
