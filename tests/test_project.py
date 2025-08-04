# TODO: Update to use new camtasio API
# from camtasio import new_project, use_project
import pytest

pytestmark = pytest.mark.skip(
    reason="Legacy project functions not yet implemented in unified package"
)


def test_file_path(simple_video_path, simple_video):
    assert simple_video_path.absolute() == simple_video.file_path.absolute()


def test_authoring_client(simple_video):
    ac = simple_video.authoring_client
    assert ac.name == "Camtasia"
    assert ac.platform == "Mac"
    assert ac.version == "2019.0.1"


def test_edit_rate(simple_video):
    assert simple_video.edit_rate == 30


def test_use_project(simple_video_path):
    # TODO: Uncomment when use_project function is implemented
    # with use_project(simple_video_path) as proj:
    #     test_file_path(simple_video_path, proj)
    #     test_authoring_client(proj)
    #     test_edit_rate(proj)
    pass


# TODO: Test use_project(save_on_exit=True/False)


def test_new_project_creates_cmproj(temp_path):
    project_path = temp_path / "temp.cmproj"
    assert not project_path.exists()
    # TODO: Uncomment when new_project function is implemented
    # new_project(project_path)
    # assert project_path.exists()
    # assert (project_path / "project.tscproj").exists()
    pass
