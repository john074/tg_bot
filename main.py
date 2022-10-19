import telebot
import download_audio
import threading

bot = telebot.TeleBot("")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome to the bot\nType a link to a video to get the audio file")


@bot.message_handler(content_types=['text'])
def check_message(message):
    if message.text.startswith('https://www.youtube.com/') or message.text.startswith('youtube.com/')\
            or message.text.startswith('https://youtu.be/') or message.text.startswith('youtu.be/'):
        bot.send_message(message.chat.id, "Processing...\nIt may take a minute")
        threading.Thread(target=download_audio.download_audio,
                         args=(message.text, message.chat.id, bot)).start()


bot.infinity_polling()
