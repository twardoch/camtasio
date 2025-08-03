import hypothesis.strategies as st
from hypothesis import given

from camtasia.frame_stamp import FrameStamp


@st.composite
def frame_stamps(draw):
    return FrameStamp(
        frame_number=draw(st.integers(min_value=0, max_value=1000000000)),
        frame_rate=draw(st.integers(min_value=1)))


@given(frame_stamps())
def test_sub_frames_are_less_than_frame_rate(fstamp):
    _, subframes = fstamp.frame_time
    assert subframes < fstamp.frame_rate


@given(frame_stamps())
def test_frame_times_add_up_to_frame_number(fstamp):
    tdelta, subframes = fstamp.frame_time
    assert tdelta.total_seconds() * fstamp.frame_rate + subframes == fstamp.frame_number
