import pytube
import os
from pydub import AudioSegment
import time
import threading


def download_audio(url, chat, bot):
    vid = pytube.YouTube(url)
    f = vid.streams.filter(only_audio=True).order_by("abr").desc().first().download()
    if os.path.getsize(f.title()) > 51380224:
        split_audio(f.title(), chat, bot)
    else:
        send_audio([f.title()], chat, bot)


def split_audio(file, chat, bot):
    print("in split")
    audio = AudioSegment.from_file(file)
    parts = os.path.getsize(file) // 40380224 + 1
    break_point = len(audio) // parts
    files = []
    for i in range(parts):
        print(i)
        audio[i * break_point: (i + 1) * break_point].export("part" + str(i) + ".webm", format="webm")
        files.append("part" + str(i) + ".webm")

    send_audio(files, chat, bot)


def send_audio(files, chat, bot):
    print("in send")
    for i in files:
        audio = open(i, 'rb')
        bot.send_audio(chat, audio)
        audio.close()
        os.remove(i)
