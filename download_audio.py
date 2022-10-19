import yt_dlp
from pydub import AudioSegment
import os
import threading
import time

ydl_opts = {
    'format': 'm4a/bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
    'outtmpl': '1.mp3',
}


def download_audio(url, chat_id, bot):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    if os.path.getsize('1.mp3') > 51380224:
        split_audio(chat_id, bot)
    else:
        send_audio(chat_id, bot)


def send_audio(chat_id, bot, amount=1):
    if amount == 1:
        audio = open('1.mp3', 'rb')
        bot.send_audio(chat_id, audio)
    else:
        audio = open('1.mp3', 'rb')
        bot.send_audio(chat_id, audio)
        audio.close()
        audio = open('2.mp3', 'rb')
        bot.send_audio(chat_id, audio)
        audio.close()

    threading.Thread(target=clean_up).start()


def split_audio(chat_id, bot):
    sound = AudioSegment.from_mp3("1.mp3")
    halfway_point = len(sound) / 2

    first_half = sound[:halfway_point]
    second_half = sound[halfway_point:]

    first_half.export("1.mp3", format="mp3")
    second_half.export("2.mp3", format="mp3")

    send_audio(chat_id, bot, 2)


def clean_up():
    time.sleep(10)
    os.remove('1.mp3')
    if os.path.exists('2.mp3'):
        os.remove('2.mp3')
