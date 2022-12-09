import numpy as np
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.tools.drawing import color_gradient


def generate_vid(size=(124, 124), timestamps=[], clip_duration=10, video_name="test", audio_name="foo"):
    grad = color_gradient(size,
                          p1=tuple(np.random.randint(0, size[0], (1, 2)).flatten()),
                          p2=tuple(np.random.randint(0, size[0], (1, 2)).flatten()),
                          col1=np.random.randint(0, 255, (1, 3)).flatten().tolist(),
                          col2=np.random.randint(0, 255, (1, 3)).flatten().tolist(),
                          shape='linear')
    picture = ImageClip(grad, transparent=True).set_duration(clip_duration)

    duration = 0.3
    txt_clips = []
    for i, timestamp in enumerate(timestamps):
        # txt_clip = TextClip("BEAT", fontsize=size[0] / 16, color='white')
        grad = color_gradient(size,
                              p1=tuple(np.random.randint(0, size[0], (1, 2)).flatten()),
                              p2=tuple(np.random.randint(0, size[0], (1, 2)).flatten()),
                              col1=np.random.randint(0, 255, (1, 3)).flatten().tolist(),
                              col2=np.random.randint(0, 255, (1, 3)).flatten().tolist(),
                              shape='linear')
        txt_clip = ImageClip(grad, transparent=True)
        txt_clip = txt_clip.set_start(timestamp)
        txt_clip = txt_clip.set_pos('center').set_duration(duration)
        txt_clips.append(txt_clip)

    audio = AudioFileClip(f"{audio_name}_cut.wav").subclip(0, clip_duration)
    video_with_new_audio = picture.set_audio(audio)
    final_video = CompositeVideoClip([video_with_new_audio] + txt_clips)
    final_video.write_videofile(f"{video_name}.mp4", fps=24, threads=4)


if __name__ == '__main__':
    pass