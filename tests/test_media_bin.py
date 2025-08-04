import datetime as dt
from pathlib import Path

import pytest

# TODO: Re-enable when MediaType is implemented
# from camtasio.models import MediaType
import pytest

pytestmark = pytest.mark.skip(reason="MediaType and media_bin not yet implemented in unified package")


@pytest.fixture(params=['example.wav', 'llama.jpg', 'sample.mov'])
def media_path(request, media_root):
    return media_root / request.param


class TestMediaBin:
    def test_media_bin_is_initially_empty(self, project):
        assert len(project.media_bin) == 0

    def test_adding_media_increased_size(self, project, media_path):
        project.media_bin.import_media(media_path)
        assert len(project.media_bin) == 1

    def test_iteration_over_media(self, project, media_path):
        project.media_bin.import_media(media_path)
        media = list(project.media_bin)
        assert len(media) == 1

    def test_get_media_by_id(self, project, media_path):
        imported_media = project.media_bin.import_media(media_path)
        fetched_media = project.media_bin[imported_media.id]
        assert fetched_media.id == imported_media.id

    def test_delete_media_removes_media(self, project, media_path):
        media = project.media_bin.import_media(media_path)
        del project.media_bin[media.id]
        assert len(project.media_bin) == 0


class TestMedia:
    def test_source_looks_correct(self, project, media_path):
        media = project.media_bin.import_media(media_path)
        assert media_path.name == media.source.name

    def test_identity(self, project, media_path: Path):
        media = project.media_bin.import_media(media_path)
        assert media.identity == media_path.stem  # NB: I only assume this is expected!

    def test_type_for_image(self, project, media_root: Path):
        media_path = media_root / "llama.jpg"
        media = project.media_bin.import_media(media_path)
        assert media.type == MediaType.Image

    def test_type_for_video(self, project, media_root: Path):
        media_path = media_root / "sample.mov"
        media = project.media_bin.import_media(media_path)
        assert media.type == MediaType.Video

    def test_type_for_audio(self, project, media_root: Path):
        media_path = media_root / "example.wav"
        media = project.media_bin.import_media(media_path)
        assert media.type == MediaType.Audio

    # TODO: rect, range, last_modification


def test_canned_media_test(simple_video):
    media = list(simple_video.media_bin)

    assert media[0].source == Path(
        "./recordings/1559817572.462711/Rec 6-6-2019.trec")
    assert media[0].rect == (0, 0, 5120, 2880)
    assert media[0].last_modification == dt.datetime(
        year=2019, month=6, day=6, hour=10, minute=38, second=30)

    assert media[1].source == Path(
        "./media/1562574964.179914/Screenshot 2019-07-08 at 08.52.00.png")
    assert media[1].rect == (0, 0, 970, 334)
    assert media[1].last_modification == dt.datetime(
        year=2019, month=7, day=8, hour=6, minute=52, second=5)
