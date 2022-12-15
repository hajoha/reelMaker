from audio.audio import cut_file, get_timestamps, get_timestamps_essentia
from video import video
import os

if __name__ == '__main__':
    os.chdir("files")
    #cut_len = cut_file("00:01:27:00", "00:01:45:00", "foo.wav")
    #beats, timestamps = get_timestamps("foo_cut.wav")
    #video.generate_vid(size=(1024, 1024), timestamps=timestamps,
    #                   clip_duration=cut_len,
    #                   video_name="foo_out",
    #                   audio_name="foo")
    cut_len = cut_file("00:02:06:07", "00:02:31:08", "flume.wav")
    beats, timestamps = get_timestamps_essentia("flume_cut.wav")
    print(f"timestamps: {timestamps}")
    print(f"images: {len(timestamps)}")
    print(f"length: {cut_len}")
    video.generate_vid(size=(1024, 1024), timestamps=timestamps,
                      clip_duration=cut_len,
                      video_name="flume_out",
                      audio_name="flume")
