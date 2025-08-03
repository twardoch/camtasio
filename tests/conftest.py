import pathlib

import pytest

from camtasio.serialization import ProjectLoader
from camtasio.models import Project


@pytest.fixture
def media_root(pytestconfig):
    root = pathlib.Path(str(pytestconfig.rootdir))
    return root / 'tests' / 'resources' / 'media'


@pytest.fixture(scope='session')
def simple_video_path(pytestconfig):
    "Path to simple_video.cmproj."
    root = pathlib.Path(str(pytestconfig.rootdir))
    return root / 'tests' / 'resources' / 'simple-video.cmproj'


@pytest.fixture(scope='session')
def simple_video(simple_video_path):
    "The 'simple-video' Project."
    loader = ProjectLoader()
    return loader.load(simple_video_path / 'project.tscproj')


@pytest.fixture
def temp_path(tmpdir):
    return pathlib.Path(str(tmpdir))


@pytest.fixture
def project(temp_path):
    "Create a basic test project."
    # For now, return None as new_project functionality needs to be implemented
    # This fixture can be updated when project creation is added
    return None
