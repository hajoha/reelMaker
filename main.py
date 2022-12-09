from audio.audio import cut_file, get_timestamps
from video import video
import os

if __name__ == '__main__':
    os.chdir("files")
    cut_len = cut_file("00:01:27:00", "00:01:45:00", "foo.wav")
    beats, timestamps = get_timestamps("foo_cut.wav")
    video.generate_vid(size=(124, 124), timestamps=timestamps,
                       clip_duration=cut_len,
                       video_name="foo_out",
                       audio_name="foo")
