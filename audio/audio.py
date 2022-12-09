import librosa as lr
import numpy as np
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import TextClip, ColorClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.tools.drawing import color_gradient
from pydub import AudioSegment


def get_timestamps(file):
    y, sr = lr.load(file)
    onset_env = lr.onset.onset_strength(y=y, sr=sr, aggregate=np.median)
    tempo, beats = lr.beat.beat_track(bpm=120, y=y, sr=sr, hop_length=512, onset_envelope=onset_env)
    print(f'bpm:{tempo}')
    ts = lr.frames_to_time(beats, sr=sr)
    ts = [0]+ts
    return len(ts), ts


def string_to_milisecs(t):
    hours, minutes, seconds, miliseconds = (["0", "0"] + t.split(":"))[-4:]
    hours = int(hours)
    minutes = int(minutes)
    seconds = float(seconds)
    return int(3600000 * hours + 60000 * minutes + 1000 * seconds + float(miliseconds))


def cut_file(t1, t2, file):
    newAudio = AudioSegment.from_wav(file)
    newAudio = newAudio[string_to_milisecs(t1):string_to_milisecs(t2)]
    newAudio.export(f'{file.split(".")[0]}_cut.wav', format="wav")
    return newAudio.duration_seconds


if __name__ == '__main__':
    cut_len = cut_file("00:01:23:00", "00:01:40:00", "foo.wav")

    beats, timestamps = get_timestamps("foo_cut.wav")
    SIZE = (2048, 2048)
    COLOR = (0, 0, 0)
    picture = ColorClip(SIZE, COLOR, duration=cut_len)

    duration = 0.3
    txt_clips = []
    for i, timestamp in enumerate(timestamps):
        #txt_clip = TextClip("BEAT", fontsize=SIZE[0] / 16, color='white')
        grad = color_gradient(SIZE,
                              p1=tuple(np.random.randint(0, SIZE[0], (1, 2)).flatten()),
                              p2=tuple(np.random.randint(0, SIZE[0], (1, 2)).flatten()),
                              col1=np.random.randint(0, 255, (1, 3)).flatten().tolist(),
                              col2=np.random.randint(0, 255, (1, 3)).flatten().tolist(),
                              offset=0.5, shape='linear')
        txt_clip = ImageClip(grad,transparent=True)
        txt_clip = txt_clip.set_start(timestamp)
        txt_clip = txt_clip.set_pos('center').set_duration(duration)
        txt_clips.append(txt_clip)

    audio = AudioFileClip(r"foo_cut.wav").subclip(0, cut_len)

    video_with_new_audio = picture.set_audio(audio)

    final_video = CompositeVideoClip([video_with_new_audio] + txt_clips)

    final_video.write_videofile("TEXT.mp4", fps=24, threads=4)
