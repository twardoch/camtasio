# this_file: tests/test_media_models.py
"""Comprehensive tests for media models."""


from camtasio.models.media import AudioMedia, Callout, ImageMedia, VideoMedia


class TestVideoMedia:
    """Test VideoMedia class comprehensively."""

    def test_get_type_default(self):
        """Test get_type returns default VMFile."""
        media = VideoMedia(id=1, src=1)
        assert media.get_type() == "VMFile"

    def test_get_type_from_attributes(self):
        """Test get_type uses _type from attributes."""
        media = VideoMedia(id=1, src=1, attributes={"_type": "ScreenVMFile"})
        assert media.get_type() == "ScreenVMFile"

    def test_to_dict_minimal(self):
        """Test to_dict with minimal data."""
        media = VideoMedia(id=1, src=2)
        result = media.to_dict()

        expected = {
            "id": 1,
            "_type": "VMFile",
            "src": 2,
            "trackNumber": 0,
            "start": 0,
            "duration": 0,
            "mediaStart": 0,
            "mediaDuration": 0,
            "scalar": 1.0
        }
        assert result == expected

    def test_to_dict_with_all_fields(self):
        """Test to_dict with all fields populated."""
        media = VideoMedia(
            id=1, src=2, track_number=3, start=100, duration=200,
            media_start=50, media_duration=150, scalar=1.5,
            attributes={"visible": True},
            parameters={"opacity": 0.8},
            effects=[{"type": "blur"}],
            metadata={"filename": "test.mp4"},
            animation_tracks={"position": []}
        )
        result = media.to_dict()

        assert result["id"] == 1
        assert result["src"] == 2
        assert result["trackNumber"] == 3
        assert result["start"] == 100
        assert result["duration"] == 200
        assert result["mediaStart"] == 50
        assert result["mediaDuration"] == 150
        assert result["scalar"] == 1.5
        assert result["attributes"] == {"visible": True}
        assert result["parameters"] == {"opacity": 0.8}
        assert result["effects"] == [{"type": "blur"}]
        assert result["metadata"] == {"filename": "test.mp4"}
        assert result["animationTracks"] == {"position": []}

    def test_scale_spatial_basic_parameters(self):
        """Test spatial scaling of basic parameters."""
        media = VideoMedia(
            id=1, src=1,
            parameters={
                "translation0": 100,
                "translation1": 200,
                "translation2": 300,
                "scale0": 1.0,
                "scale1": 2.0,
                "scale2": 3.0,
                "geometryCrop0": 10,
                "geometryCrop1": 20,
                "geometryCrop2": 30,
                "geometryCrop3": 40,
                "other_param": "unchanged"
            }
        )

        scaled = media.scale_spatial(2.0)

        # Translation parameters should be scaled
        assert scaled.parameters["translation0"] == 200
        assert scaled.parameters["translation1"] == 400
        assert scaled.parameters["translation2"] == 600

        # Scale parameters should be scaled
        assert scaled.parameters["scale0"] == 2.0
        assert scaled.parameters["scale1"] == 4.0
        assert scaled.parameters["scale2"] == 6.0

        # Crop parameters should be scaled
        assert scaled.parameters["geometryCrop0"] == 20
        assert scaled.parameters["geometryCrop1"] == 40
        assert scaled.parameters["geometryCrop2"] == 60
        assert scaled.parameters["geometryCrop3"] == 80

        # Other parameters should be unchanged
        assert scaled.parameters["other_param"] == "unchanged"

    def test_scale_spatial_with_keyframes(self):
        """Test spatial scaling with keyframes."""
        media = VideoMedia(
            id=1, src=1,
            parameters={
                "translation0": {
                    "keyframes": [
                        {"time": 0, "value": 100},
                        {"time": 1000, "value": 200}
                    ]
                },
                "scale1": {
                    "keyframes": [
                        {"time": 500, "value": 1.5},
                        {"time": 2000, "value": 2.0}
                    ]
                },
                "non_spatial": {
                    "keyframes": [
                        {"time": 0, "value": 0.5}
                    ]
                }
            }
        )

        scaled = media.scale_spatial(2.0)

        # Spatial keyframes should be scaled
        translation_kf = scaled.parameters["translation0"]["keyframes"]
        assert translation_kf[0]["value"] == 200  # 100 * 2
        assert translation_kf[1]["value"] == 400  # 200 * 2

        scale_kf = scaled.parameters["scale1"]["keyframes"]
        assert scale_kf[0]["value"] == 3.0  # 1.5 * 2
        assert scale_kf[1]["value"] == 4.0  # 2.0 * 2

        # Non-spatial keyframes should not be scaled
        non_spatial_kf = scaled.parameters["non_spatial"]["keyframes"]
        assert non_spatial_kf[0]["value"] == 0.5  # unchanged

    def test_scale_temporal_basic(self):
        """Test temporal scaling of basic properties."""
        media = VideoMedia(
            id=1, src=1,
            start=100, duration=200,
            media_start=50, media_duration=150
        )

        scaled = media.scale_temporal(2.0)

        assert scaled.start == 200  # 100 * 2
        assert scaled.duration == 400  # 200 * 2
        assert scaled.media_start == 100  # 50 * 2
        assert scaled.media_duration == 300  # 150 * 2

    def test_scale_temporal_with_string_media_values(self):
        """Test temporal scaling with string media values."""
        media = VideoMedia(
            id=1, src=1,
            start=100, duration=200,
            media_start="auto", media_duration="full"
        )

        scaled = media.scale_temporal(2.0)

        assert scaled.start == 200
        assert scaled.duration == 400
        # String values should be preserved
        assert scaled.media_start == "auto"
        assert scaled.media_duration == "full"

    def test_scale_temporal_with_keyframes(self):
        """Test temporal scaling with keyframes."""
        media = VideoMedia(
            id=1, src=1,
            parameters={
                "opacity": {
                    "keyframes": [
                        {"time": 100, "value": 0.0},
                        {"time": 500, "endTime": 1000, "duration": 500, "value": 1.0}
                    ]
                }
            }
        )

        scaled = media.scale_temporal(2.0)

        keyframes = scaled.parameters["opacity"]["keyframes"]
        assert keyframes[0]["time"] == 200  # 100 * 2
        assert keyframes[1]["time"] == 1000  # 500 * 2
        assert keyframes[1]["endTime"] == 2000  # 1000 * 2
        assert keyframes[1]["duration"] == 1000  # 500 * 2

    def test_scale_temporal_keyframes_with_non_numeric_values(self):
        """Test temporal scaling ignores non-numeric keyframe values."""
        media = VideoMedia(
            id=1, src=1,
            parameters={
                "test": {
                    "keyframes": [
                        {"time": "auto", "value": 1.0},
                        {"time": 100, "endTime": "end", "duration": None, "value": 0.5}
                    ]
                }
            }
        )

        scaled = media.scale_temporal(2.0)

        keyframes = scaled.parameters["test"]["keyframes"]
        # Non-numeric values should be preserved
        assert keyframes[0]["time"] == "auto"
        assert keyframes[1]["endTime"] == "end"
        assert keyframes[1]["duration"] is None
        # Numeric values should be scaled
        assert keyframes[1]["time"] == 200  # 100 * 2

    def test_scale_preserves_other_fields(self):
        """Test that scaling preserves all other fields."""
        media = VideoMedia(
            id=1, src=2, track_number=3,
            scalar="custom",
            attributes={"visible": True},
            effects=[{"type": "blur"}],
            metadata={"filename": "test.mp4"},
            animation_tracks={"position": []}
        )

        spatial_scaled = media.scale_spatial(2.0)
        temporal_scaled = media.scale_temporal(0.5)

        for scaled in [spatial_scaled, temporal_scaled]:
            assert scaled.id == 1
            assert scaled.src == 2
            assert scaled.track_number == 3
            assert scaled.scalar == "custom"
            assert scaled.attributes == {"visible": True}
            assert scaled.effects == [{"type": "blur"}]
            assert scaled.metadata == {"filename": "test.mp4"}
            assert scaled.animation_tracks == {"position": []}


class TestAudioMedia:
    """Test AudioMedia class comprehensively."""

    def test_get_type(self):
        """Test get_type returns AMFile."""
        media = AudioMedia(id=1, src=1)
        assert media.get_type() == "AMFile"

    def test_to_dict_with_channel_number(self):
        """Test to_dict includes channel number."""
        media = AudioMedia(id=1, src=2, channel_number="0")
        result = media.to_dict()

        assert result["channelNumber"] == "0"
        assert result["_type"] == "AMFile"

    def test_scale_spatial_no_changes(self):
        """Test spatial scaling doesn't change audio parameters."""
        media = AudioMedia(
            id=1, src=1,
            parameters={"volume": 0.8, "translation0": 100}
        )

        scaled = media.scale_spatial(2.0)

        # Audio should not scale spatial parameters
        assert scaled.parameters == {"volume": 0.8, "translation0": 100}

    def test_scale_temporal_preserves_duration(self):
        """Test temporal scaling preserves audio duration."""
        media = AudioMedia(
            id=1, src=1,
            start=100, duration=200,
            media_start=50, media_duration=150
        )

        scaled = media.scale_temporal(2.0)

        # Only start should be scaled
        assert scaled.start == 200  # 100 * 2
        # Duration and media values should be preserved
        assert scaled.duration == 200  # unchanged
        assert scaled.media_start == 50  # unchanged
        assert scaled.media_duration == 150  # unchanged

    def test_scale_temporal_with_keyframes(self):
        """Test temporal scaling of audio keyframes (e.g., volume fades)."""
        media = AudioMedia(
            id=1, src=1,
            parameters={
                "volume": {
                    "keyframes": [
                        {"time": 100, "value": 0.0},
                        {"time": 500, "value": 1.0}
                    ]
                }
            }
        )

        scaled = media.scale_temporal(2.0)

        keyframes = scaled.parameters["volume"]["keyframes"]
        assert keyframes[0]["time"] == 200  # 100 * 2
        assert keyframes[1]["time"] == 1000  # 500 * 2

    def test_default_channel_number(self):
        """Test default channel number."""
        media = AudioMedia(id=1, src=1)
        assert media.channel_number == "0,1"

    def test_custom_channel_number(self):
        """Test custom channel number."""
        media = AudioMedia(id=1, src=1, channel_number="1")
        assert media.channel_number == "1"

        result = media.to_dict()
        assert result["channelNumber"] == "1"


class TestImageMedia:
    """Test ImageMedia class comprehensively."""

    def test_get_type(self):
        """Test get_type returns IMFile."""
        media = ImageMedia(id=1, src=1)
        assert media.get_type() == "IMFile"

    def test_to_dict_with_trim_start_sum(self):
        """Test to_dict includes trimStartSum when non-zero."""
        media = ImageMedia(id=1, src=2, trim_start_sum=100)
        result = media.to_dict()

        assert result["trimStartSum"] == 100
        assert result["_type"] == "IMFile"

    def test_to_dict_without_trim_start_sum(self):
        """Test to_dict excludes trimStartSum when zero."""
        media = ImageMedia(id=1, src=2, trim_start_sum=0)
        result = media.to_dict()

        assert "trimStartSum" not in result

    def test_scale_spatial(self):
        """Test spatial scaling of image media."""
        media = ImageMedia(
            id=1, src=1,
            parameters={"translation0": 100, "scale0": 1.5}
        )

        scaled = media.scale_spatial(2.0)

        assert scaled.parameters["translation0"] == 200
        assert scaled.parameters["scale0"] == 3.0

    def test_scale_temporal_with_trim(self):
        """Test temporal scaling includes trim_start_sum."""
        media = ImageMedia(
            id=1, src=1,
            start=100, duration=200,
            trim_start_sum=50
        )

        scaled = media.scale_temporal(2.0)

        assert scaled.start == 200  # 100 * 2
        assert scaled.duration == 400  # 200 * 2
        assert scaled.trim_start_sum == 100  # 50 * 2

    def test_default_trim_start_sum(self):
        """Test default trim_start_sum."""
        media = ImageMedia(id=1, src=1)
        assert media.trim_start_sum == 0


class TestCallout:
    """Test Callout class comprehensively."""

    def test_get_type(self):
        """Test get_type returns Callout."""
        callout = Callout(id=1, src=0)
        assert callout.get_type() == "Callout"

    def test_to_dict_with_definition(self):
        """Test to_dict includes definition."""
        callout = Callout(
            id=1, src=0,
            definition={"kind": "text", "text": "Hello"}
        )
        result = callout.to_dict()

        assert result["def"] == {"kind": "text", "text": "Hello"}
        assert result["_type"] == "Callout"

    def test_to_dict_without_definition(self):
        """Test to_dict excludes empty definition."""
        callout = Callout(id=1, src=0, definition={})
        result = callout.to_dict()

        assert "def" not in result

    def test_text_class_method_basic(self):
        """Test Callout.text class method with basic parameters."""
        callout = Callout.text("Hello World")

        assert callout.id == 0
        assert callout.src == 0
        assert callout.definition["kind"] == "text"
        assert callout.definition["text"] == "Hello World"
        assert callout.definition["font-size"] == 24

    def test_text_class_method_with_style(self):
        """Test Callout.text class method with style parameters."""
        callout = Callout.text(
            "Styled Text",
            font_size=36,
            color="#FF0000",
            weight="bold"
        )

        assert callout.definition["text"] == "Styled Text"
        assert callout.definition["font-size"] == 36
        assert callout.definition["color"] == "#FF0000"
        assert callout.definition["weight"] == "bold"

    def test_scale_spatial_definition(self):
        """Test spatial scaling of callout definition."""
        callout = Callout(
            id=1, src=0,
            definition={
                "width": 100,
                "height": 50,
                "corner-radius": 5,
                "stroke-width": 2,
                "text": "Hello",  # Should not be scaled
                "color": "#FF0000"  # Should not be scaled
            }
        )

        scaled = callout.scale_spatial(2.0)

        # Spatial properties should be scaled
        assert scaled.definition["width"] == 200  # 100 * 2
        assert scaled.definition["height"] == 100  # 50 * 2
        assert scaled.definition["corner-radius"] == 10  # 5 * 2
        assert scaled.definition["stroke-width"] == 4  # 2 * 2

        # Non-spatial properties should be preserved
        assert scaled.definition["text"] == "Hello"
        assert scaled.definition["color"] == "#FF0000"

    def test_scale_spatial_missing_definition_keys(self):
        """Test spatial scaling when definition keys are missing."""
        callout = Callout(
            id=1, src=0,
            definition={"text": "Hello"}  # No spatial properties
        )

        scaled = callout.scale_spatial(2.0)

        # Definition should be unchanged
        assert scaled.definition == {"text": "Hello"}

    def test_scale_temporal(self):
        """Test temporal scaling of callout."""
        callout = Callout(
            id=1, src=0,
            start=100, duration=200,
            parameters={
                "opacity": {
                    "keyframes": [
                        {"time": 100, "value": 0.0},
                        {"time": 200, "value": 1.0}
                    ]
                }
            }
        )

        scaled = callout.scale_temporal(2.0)

        assert scaled.start == 200  # 100 * 2
        assert scaled.duration == 400  # 200 * 2

        keyframes = scaled.parameters["opacity"]["keyframes"]
        assert keyframes[0]["time"] == 200  # 100 * 2
        assert keyframes[1]["time"] == 400  # 200 * 2

    def test_default_definition(self):
        """Test default empty definition."""
        callout = Callout(id=1, src=0)
        assert callout.definition == {}


class TestMediaHelperMethods:
    """Test helper methods in Media base class."""

    def test_scale_parameters_with_string_values(self):
        """Test _scale_parameters ignores string values."""
        media = VideoMedia(
            id=1, src=1,
            parameters={
                "translation0": "auto",
                "scale0": 2.0,
                "geometryCrop0": "center"
            }
        )

        scaled = media.scale_spatial(2.0)

        # String values should be preserved
        assert scaled.parameters["translation0"] == "auto"
        assert scaled.parameters["geometryCrop0"] == "center"
        # Numeric values should be scaled
        assert scaled.parameters["scale0"] == 4.0

    def test_scale_keyframes_spatial_complex(self):
        """Test _scale_keyframes_spatial with complex keyframe data."""
        media = VideoMedia(id=1, src=1)

        keyframes = [
            {"time": 0, "value": 100, "ease": "linear"},
            {"time": 1000, "value": 200, "ease": "ease-in-out"},
            {"time": 2000, "other_field": "test"}  # No value field
        ]

        scaled_keyframes = media._scale_keyframes_spatial(keyframes, 2.0)

        assert scaled_keyframes[0]["value"] == 200  # 100 * 2
        assert scaled_keyframes[0]["ease"] == "linear"  # preserved
        assert scaled_keyframes[1]["value"] == 400  # 200 * 2
        assert scaled_keyframes[1]["ease"] == "ease-in-out"  # preserved
        assert scaled_keyframes[2]["other_field"] == "test"  # preserved
        assert "value" not in scaled_keyframes[2]  # no value to scale

    def test_scale_keyframes_temporal_complex(self):
        """Test _scale_keyframes_temporal with complex keyframe data."""
        media = VideoMedia(id=1, src=1)

        keyframes = [
            {"time": 100, "endTime": 500, "duration": 400, "value": 1.0},
            {"time": "auto", "value": 0.5},  # Non-numeric time
            {"endTime": 1000, "value": 0.0},  # No time field
            {"duration": None, "value": 1.0}  # None duration
        ]

        scaled_keyframes = media._scale_keyframes_temporal(keyframes, 2.0)

        # First keyframe - all numeric values scaled
        assert scaled_keyframes[0]["time"] == 200  # 100 * 2
        assert scaled_keyframes[0]["endTime"] == 1000  # 500 * 2
        assert scaled_keyframes[0]["duration"] == 800  # 400 * 2

        # Second keyframe - non-numeric time preserved
        assert scaled_keyframes[1]["time"] == "auto"

        # Third keyframe - no time field, endTime scaled
        assert scaled_keyframes[2]["endTime"] == 2000  # 1000 * 2
        assert "time" not in scaled_keyframes[2]

        # Fourth keyframe - None duration preserved
        assert scaled_keyframes[3]["duration"] is None

    def test_to_dict_empty_collections(self):
        """Test to_dict excludes empty collections."""
        media = VideoMedia(
            id=1, src=2,
            attributes={},
            parameters={},
            effects=[],
            metadata={},
            animation_tracks={}
        )

        result = media.to_dict()

        # Empty collections should not be included
        assert "attributes" not in result
        assert "parameters" not in result
        assert "effects" not in result
        assert "metadata" not in result
        assert "animationTracks" not in result

        # Basic fields should still be present
        assert result["id"] == 1
        assert result["src"] == 2
