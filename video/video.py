import numpy as np
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx.crop import crop
from moviepy.video.fx.resize import resize
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.tools.drawing import color_gradient


def generate_vid(size=(124, 124), timestamps=[], clip_duration=10, files=[], video_name="test", audio_name="foo"):
    # grad = color_gradient(size,
    #                       p1=tuple(np.random.randint(0, size[0], (1, 2)).flatten()),
    #                       p2=tuple(np.random.randint(0, size[0], (1, 2)).flatten()),
    #                       col1=np.random.randint(0, 255, (1, 3)).flatten().tolist(),
    #                       col2=np.random.randint(0, 255, (1, 3)).flatten().tolist(),
    #                       shape='linear')
    # picture = ImageClip(grad, transparent=True).set_duration(timestamps[0])

    picture = VideoFileClip("IMG_2059.MOV")
    (w, h) = picture.size
    picture = resize(picture, newsize=size)
    picture = picture.set_duration(timestamps[1])

    n = 3
    txt_clips = []
    for i in range(0, len(timestamps), 2):
        batch_timestamp = timestamps[i:i + n]
        batch_file = files[i:i + n]
        sticker = ImageClip(batch_file[0], transparent=True)
        sticker = sticker.set_start(batch_timestamp[0])
        background = ImageClip(batch_file[1], transparent=True)
        background = background.set_start(batch_timestamp[1])

        if len(batch_file) != n:
            sticker = sticker.set_pos('center').set_duration(clip_duration - batch_timestamp[0])
            background = background.set_pos('center').set_duration(clip_duration - batch_timestamp[0])
        else:
            sticker = sticker.set_pos('center').set_duration(batch_timestamp[2] - batch_timestamp[0])
            background = background.set_pos('center').set_duration(batch_timestamp[2] - batch_timestamp[0])

        print(batch_file[0])
        # if i+1 == len(timestamps):
        #     txt_clip = txt_clip.set_pos('center').set_duration(clip_duration-timestamp)
        # else:
        #     txt_clip = txt_clip.set_pos('center').set_duration(timestamp+(timestamps[i+1]-timestamp))
        txt_clips.append(sticker)
        txt_clips.append(background)

    audio = AudioFileClip(f"{audio_name}_cut.wav")
    final_video = CompositeVideoClip([picture] + txt_clips)
    final_video = final_video.set_audio(audio)
    final_video.write_videofile(f"{video_name}.mp4", fps=24, threads=4, codec='libx264',
                                audio_codec='aac',
                                temp_audiofile='temp-audio.m4a',
                                remove_temp=True
                                )


if __name__ == '__main__':
    pass
