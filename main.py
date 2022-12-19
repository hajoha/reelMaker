import PIL

import picture.picture
from audio.audio import cut_file, get_timestamps_librosa
from video import video
from wand.image import Image
import os
from os import walk

if __name__ == '__main__':
    os.chdir("files")
    # cut_len = cut_file("00:01:27:00", "00:01:45:00", "foo.wav")
    # beats, timestamps = get_timestamps("foo_cut.wav")
    # video.generate_vid(size=(1024, 1024), timestamps=timestamps,
    #                   clip_duration=cut_len,
    #                   video_name="foo_out",
    #                   audio_name="foo")

    # cut_len = cut_file("00:02:06:07", "00:02:31:08", "flume.wav")
    # beats, timestamps = get_timestamps_essentia("flume_cut.wav")
    # print(f"timestamps: {timestamps}")
    # print(f"images: {len(timestamps)}")
    # print(f"length: {cut_len}")
    # video.generate_vid(size=(1024, 1024), timestamps=timestamps,
    #                   clip_duration=cut_len,
    #                   video_name="flume_out",
    #                   audio_name="flume")

    path = "../inFiles"
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        pass
    filenames.remove(".DS_Store")
    for file in filenames:
        file = f"{path}/{file}"
        if file.endswith(".HEIC"):
            img = Image(filename=file)
            img.format = 'JPG'
            os.remove(file)
            img.save(filename=file.replace(".HEIC", ".JPG"))
            img.close()

        image = PIL.Image.open(file)
        new_image = image.resize((1080, 1920))
        new_image.save(file)

        if file.endswith(".jpg"):
            os.rename(file, file.replace(".jpg", ".JPG"))
            continue
    print(filenames)

    # for img in filenames:
    #    picture.picture.remove_background(img,
    #                                      in_path=path,
    #                                      out_path="../outFiles")

    path = "../outFiles"
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        pass
    filenames = [f"{path}/{x}" for x in filenames]
    size = (1080, 1920)
    cut_len = cut_file("00:02:12:08", "00:02:40:08", "flume.wav")

    beats, timestamps = get_timestamps_librosa("flume_cut.wav")
    print(f"images: {len(timestamps)}")
    print(f"length: {cut_len}")
    print(filenames)
    filenames.remove('../outFiles/.DS_Store')
    filenames.sort()
    print(filenames)

    if len(timestamps) != len(filenames):
        print(f"{len(timestamps)} != {len(filenames)}")
        exit(1)
    video.generate_vid(size=size, timestamps=timestamps,
                       clip_duration=cut_len,
                       files=filenames,
                       video_name="flume_out",
                       audio_name="flume")
