import pytube
import os
from pydub import AudioSegment
import moviepy.editor as moviepy


def download_audio(url, chat, bot):
    vid = pytube.YouTube(url)
    f = vid.streams.filter(only_audio=True).order_by("abr").desc().first().download()
    file_size = os.path.getsize(f.title())
    if file_size > 51380224:
        split_audio(f.title(), chat, bot, file_size)
    else:
        send_audio([f.title()], chat, bot)


def split_audio(file, chat, bot, file_size):
    print("in split")
    clip = moviepy.AudioFileClip(file)
    clip.write_audiofile(f"{file[:-5]}.wav")
    audio = AudioSegment.from_file(f"{file[:-5]}.wav", format="wav")
    parts = file_size // 40380224 + 1
    break_point = len(audio) // parts
    files = []
    for i in range(parts):
        print(i)
        audio[i * break_point: (i + 1) * break_point].export("part" + str(i) + ".webm", format="webm")
        files.append("part" + str(i) + ".webm")

    os.remove(file)
    os.remove(f"{file[:-5]}.wav")
    send_audio(files, chat, bot)


def send_audio(files, chat, bot):
    for i in files:
        audio = open(i, 'rb')
        bot.send_audio(chat, audio)
        audio.close()
        os.remove(i)

