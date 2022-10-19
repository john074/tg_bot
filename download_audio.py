import yt_dlp
from pydub import AudioSegment
import os
import time
import threading

ydl_opts = {
    'format': 'm4a/bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
    'outtmpl': 'main.mp3',
    'playlist_items': '1',
}


def download_audio(url, chat_id, bot):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    if os.path.getsize('main.mp3') > 51380224:
        split_audio(chat_id, bot)
    else:
        os.rename('main.mp3', '0.mp3')
        send_audio(chat_id, bot)


def send_audio(chat_id, bot, amount=0):
    for i in range(amount):
        audio = open(f'{i}.mp3', 'rb')
        bot.send_audio(chat_id, audio)
        audio.close()
    threading.Thread(clean_up(amount)).start()


def split_audio(chat_id, bot):
    sound = AudioSegment.from_mp3('main.mp3')
    parts = os.path.getsize('main.mp3') // 51380224 + 1
    break_point = len(sound) / parts
    for i in range(parts):
        sound[i * break_point:(i + 1) * break_point].export(f'{i}.mp3', format='mp3')

    send_audio(chat_id, bot, parts)


def clean_up(amount):
    time.sleep(10)
    try:
        for i in range(amount + 1):
            if os.path.exists(f'{i}.mp3'):
                os.remove(f'{i}.mp3')
        os.remove('main.mp3')
    except FileNotFoundError:
        pass
