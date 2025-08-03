#!/usr/bin/env python3
"""Comprehensive tests for media operations."""
# this_file: tests/test_media_operations.py

import pytest
from unittest.mock import Mock, MagicMock
from typing import Dict, Any, List

from camtasio.operations.media_operations import (
    add_media_to_track,
    remove_media,
    duplicate_media,
    find_media_references
)


class MockTrackMedia:
    """Mock track media object."""
    
    def __init__(self, media_id: str, source: str):
        self.id = media_id
        self.source = source


class MockTrack:
    """Mock track object."""
    
    def __init__(self):
        self.medias = {}
        self._media_list = []
    
    def add_media(self, media, start_frame: int, duration=None, effects=None):
        """Mock add_media method."""
        # Simulate adding media to track
        media_id = f"track_media_{len(self._media_list)}"
        track_media = MockTrackMedia(media_id, media.id)
        self.medias[media_id] = track_media
        self._media_list.append(track_media)
        return track_media


class MockMedia:
    """Mock media object."""
    
    def __init__(self, media_id: str, name: str = "test_media"):
        self.id = media_id
        self.name = name
    
    def copy(self):
        """Create a copy of this media."""
        return MockMedia(f"{self.id}_copy", f"{self.name}_copy")


class MockTimeline:
    """Mock timeline object."""
    
    def __init__(self):
        self.tracks = []
    
    def add_track(self):
        track = MockTrack()
        self.tracks.append(track)
        return track


class MockProject:
    """Mock project object."""
    
    def __init__(self):
        self.timeline = MockTimeline()
        self.media_bin = {}
    
    def add_media_to_bin(self, media_id: str, media=None):
        if media is None:
            media = MockMedia(media_id)
        self.media_bin[media_id] = media
        return media


class TestAddMediaToTrack:
    """Test add_media_to_track function."""
    
    def test_add_media_to_track_success(self):
        """Test successful media addition to track."""
        project = MockProject()
        
        # Set up media bin
        media = project.add_media_to_bin("media1")
        
        # Set up track
        track = project.timeline.add_track()
        
        # Add media to track
        add_media_to_track(project, 0, "media1", 100)
        
        # Verify media was added
        assert len(track.medias) == 1
        track_media = list(track.medias.values())[0]
        assert track_media.source == "media1"
    
    def test_add_media_to_track_with_effects(self):
        """Test adding media to track with effects."""
        project = MockProject()
        media = project.add_media_to_bin("media1")
        track = project.timeline.add_track()
        
        # Mock effects
        effects = ["effect1", "effect2"]
        
        # Add media with effects
        add_media_to_track(project, 0, "media1", 100, duration=200, effects=effects)
        
        # Verify media was added
        assert len(track.medias) == 1
    
    def test_add_media_to_track_invalid_track_index(self):
        """Test adding media to invalid track index."""
        project = MockProject()
        project.add_media_to_bin("media1")
        
        # Try to add to non-existent track
        with pytest.raises(KeyError, match="Track index 0 not found"):
            add_media_to_track(project, 0, "media1", 100)
    
    def test_add_media_to_track_invalid_media_id(self):
        """Test adding non-existent media to track."""
        project = MockProject()
        track = project.timeline.add_track()
        
        # Try to add non-existent media
        with pytest.raises(KeyError, match="Media ID nonexistent not found"):
            add_media_to_track(project, 0, "nonexistent", 100)
    
    def test_add_media_to_track_overlap_error(self):
        """Test handling of media overlap errors."""
        project = MockProject()
        media = project.add_media_to_bin("media1")
        track = project.timeline.add_track()
        
        # Mock track to raise ValueError on overlap
        def mock_add_media_overlap(*args, **kwargs):
            raise ValueError("Media overlaps existing track media")
        
        track.add_media = mock_add_media_overlap
        
        with pytest.raises(ValueError, match="Media overlaps existing track media"):
            add_media_to_track(project, 0, "media1", 100)


class TestRemoveMedia:
    """Test remove_media function."""
    
    def test_remove_media_with_clear_tracks(self):
        """Test removing media with track reference clearing."""
        project = MockProject()
        
        # Set up media and tracks
        media = project.add_media_to_bin("media1")
        track1 = project.timeline.add_track()
        track2 = project.timeline.add_track()
        
        # Add media to tracks
        track_media1 = MockTrackMedia("tm1", "media1")
        track_media2 = MockTrackMedia("tm2", "media1")
        track1.medias["tm1"] = track_media1
        track2.medias["tm2"] = track_media2
        
        # Remove media with clear_tracks=True
        remove_media(project, "media1", clear_tracks=True)
        
        # Verify media removed from bin
        assert "media1" not in project.media_bin
        
        # Verify track references removed
        assert "tm1" not in track1.medias
        assert "tm2" not in track2.medias
    
    def test_remove_media_without_clear_tracks_with_references(self):
        """Test removing media without clearing tracks when references exist."""
        project = MockProject()
        
        # Set up media and tracks
        media = project.add_media_to_bin("media1")
        track = project.timeline.add_track()
        
        # Add media to track
        track_media = MockTrackMedia("tm1", "media1")
        track.medias["tm1"] = track_media
        
        # Try to remove media without clearing tracks
        with pytest.raises(ValueError, match="Cannot remove media media1.*track references"):
            remove_media(project, "media1", clear_tracks=False)
        
        # Verify media still in bin
        assert "media1" in project.media_bin
    
    def test_remove_media_without_clear_tracks_no_references(self):
        """Test removing media without clearing tracks when no references exist."""
        project = MockProject()
        
        # Set up media without track references
        media = project.add_media_to_bin("media1")
        
        # Remove media without clearing tracks
        remove_media(project, "media1", clear_tracks=False)
        
        # Verify media removed from bin
        assert "media1" not in project.media_bin
    
    def test_remove_media_nonexistent(self):
        """Test removing non-existent media."""
        project = MockProject()
        
        with pytest.raises(KeyError, match="Media ID nonexistent not found"):
            remove_media(project, "nonexistent")
    
    def test_remove_media_no_references(self):
        """Test removing media with no track references."""
        project = MockProject()
        
        # Set up media without references
        media = project.add_media_to_bin("media1")
        
        # Remove media
        remove_media(project, "media1")
        
        # Verify media removed
        assert "media1" not in project.media_bin


class TestDuplicateMedia:
    """Test duplicate_media function."""
    
    def test_duplicate_media_success(self):
        """Test successful media duplication."""
        project = MockProject()
        
        # Set up original media
        original_media = project.add_media_to_bin("media1")
        
        # Duplicate media
        new_id = duplicate_media(project, "media1")
        
        # Verify new media exists
        assert new_id in project.media_bin
        assert new_id != "media1"
        assert new_id.startswith("media1_copy")
        
        # Verify original still exists
        assert "media1" in project.media_bin
    
    def test_duplicate_media_with_custom_id(self):
        """Test duplicating media with custom ID."""
        project = MockProject()
        
        # Set up original media
        original_media = project.add_media_to_bin("media1")
        
        # Duplicate media with custom ID
        new_id = duplicate_media(project, "media1", "custom_media")
        
        # Verify new media has custom ID
        assert new_id == "custom_media"
        assert "custom_media" in project.media_bin
    
    def test_duplicate_media_nonexistent_source(self):
        """Test duplicating non-existent media."""
        project = MockProject()
        
        with pytest.raises(KeyError, match="Source media ID nonexistent not found"):
            duplicate_media(project, "nonexistent")
    
    def test_duplicate_media_id_already_exists(self):
        """Test duplicating media with existing target ID."""
        project = MockProject()
        
        # Set up media
        project.add_media_to_bin("media1")
        project.add_media_to_bin("existing_media")
        
        with pytest.raises(ValueError, match="Media ID existing_media already exists"):
            duplicate_media(project, "media1", "existing_media")
    
    def test_duplicate_media_auto_increment_id(self):
        """Test auto-incrementing duplicate IDs."""
        project = MockProject()
        
        # Set up original media
        project.add_media_to_bin("media1")
        
        # Create first duplicate (should get media1_copy_1)
        id1 = duplicate_media(project, "media1")
        
        # Create conflicting media to test increment
        project.media_bin["media1_copy_1"] = MockMedia("media1_copy_1")
        
        # Create second duplicate (should get media1_copy_2)
        id2 = duplicate_media(project, "media1")
        
        # Verify IDs are different and incremented
        assert id1.startswith("media1_copy")
        assert id2.startswith("media1_copy")
        assert id1 != id2


class TestFindMediaReferences:
    """Test find_media_references function."""
    
    def test_find_media_references_with_references(self):
        """Test finding media references when they exist."""
        project = MockProject()
        
        # Set up media and tracks
        media = project.add_media_to_bin("media1")
        track1 = project.timeline.add_track()
        track2 = project.timeline.add_track()
        
        # Add media references to tracks
        track_media1 = MockTrackMedia("tm1", "media1")
        track_media2 = MockTrackMedia("tm2", "media1")
        track_media3 = MockTrackMedia("tm3", "other_media")  # Different media
        
        track1.medias["tm1"] = track_media1
        track1.medias["tm3"] = track_media3
        track2.medias["tm2"] = track_media2
        
        # Find references
        references = find_media_references(project, "media1")
        
        # Should find 2 references to media1
        assert len(references) == 2
        assert (0, "tm1") in references  # track 0, media tm1
        assert (1, "tm2") in references  # track 1, media tm2
        assert (0, "tm3") not in references  # Different media
    
    def test_find_media_references_no_references(self):
        """Test finding media references when none exist."""
        project = MockProject()
        
        # Set up media without references
        media = project.add_media_to_bin("media1")
        project.timeline.add_track()  # Empty track
        
        # Find references
        references = find_media_references(project, "media1")
        
        # Should find no references
        assert len(references) == 0
    
    def test_find_media_references_nonexistent_media(self):
        """Test finding references for non-existent media."""
        project = MockProject()
        
        with pytest.raises(KeyError, match="Media ID nonexistent not found"):
            find_media_references(project, "nonexistent")
    
    def test_find_media_references_multiple_tracks(self):
        """Test finding references across multiple tracks."""
        project = MockProject()
        
        # Set up media and multiple tracks
        media = project.add_media_to_bin("media1")
        
        # Create 5 tracks
        for i in range(5):
            project.timeline.add_track()
        
        # Add references in tracks 1, 3, and 4
        track_media1 = MockTrackMedia("tm1", "media1")
        track_media2 = MockTrackMedia("tm2", "media1")
        track_media3 = MockTrackMedia("tm3", "media1")
        
        project.timeline.tracks[1].medias["tm1"] = track_media1
        project.timeline.tracks[3].medias["tm2"] = track_media2
        project.timeline.tracks[4].medias["tm3"] = track_media3
        
        # Find references
        references = find_media_references(project, "media1")
        
        # Should find references in tracks 1, 3, 4
        assert len(references) == 3
        assert (1, "tm1") in references
        assert (3, "tm2") in references
        assert (4, "tm3") in references


class TestMediaOperationsIntegration:
    """Test integration between media operations."""
    
    def test_add_and_remove_media_workflow(self):
        """Test complete workflow of adding and removing media."""
        project = MockProject()
        
        # Add media to bin
        media = project.add_media_to_bin("media1")
        
        # Add track and media to track
        track = project.timeline.add_track()
        add_media_to_track(project, 0, "media1", 100)
        
        # Verify media is referenced
        references = find_media_references(project, "media1")
        assert len(references) == 1
        
        # Remove media with track clearing
        remove_media(project, "media1", clear_tracks=True)
        
        # Verify media and references are gone
        assert "media1" not in project.media_bin
        assert len(track.medias) == 0
    
    def test_duplicate_and_reference_workflow(self):
        """Test duplicating media and using the duplicate."""
        project = MockProject()
        
        # Add original media
        original_media = project.add_media_to_bin("media1")
        
        # Duplicate media
        duplicate_id = duplicate_media(project, "media1", "media1_dup")
        
        # Add both to tracks
        track1 = project.timeline.add_track()
        track2 = project.timeline.add_track()
        
        add_media_to_track(project, 0, "media1", 100)
        add_media_to_track(project, 1, "media1_dup", 200)
        
        # Verify both have references
        orig_refs = find_media_references(project, "media1")
        dup_refs = find_media_references(project, "media1_dup")
        
        assert len(orig_refs) == 1
        assert len(dup_refs) == 1
        
        # Remove original, keep duplicate
        remove_media(project, "media1", clear_tracks=True)
        
        # Verify only duplicate remains
        assert "media1" not in project.media_bin
        assert "media1_dup" in project.media_bin
        assert len(track1.medias) == 0  # Original reference removed
        assert len(track2.medias) == 1  # Duplicate reference remains


class TestMediaOperationsErrorHandling:
    """Test error handling in media operations."""
    
    def test_operations_with_invalid_project_structure(self):
        """Test operations with malformed project structure."""
        # Create project with missing attributes
        project = Mock()
        project.media_bin = {}
        project.timeline = Mock()
        project.timeline.tracks = []
        
        # Should handle gracefully
        with pytest.raises(KeyError):
            add_media_to_track(project, 0, "media1", 100)
    
    def test_operations_with_none_values(self):
        """Test operations with None values."""
        project = MockProject()
        
        # Test with None media ID
        with pytest.raises((KeyError, TypeError)):
            add_media_to_track(project, 0, None, 100)
    
    def test_operations_with_empty_strings(self):
        """Test operations with empty string IDs."""
        project = MockProject()
        
        # Test with empty media ID
        with pytest.raises(KeyError):
            add_media_to_track(project, 0, "", 100)