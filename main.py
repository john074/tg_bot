import telebot
import download_audio
import paymеnts
import threading

bot = telebot.TeleBot("5504530111:AAEffGN-dgcJs8gOGdiUGvAygjF_QKxGqMw")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome to the bot\nType a link to a video to get the audio file")


@bot.message_handler(commands=['buy'])
def command_pay(message):
    print("!")
    paymеnts.send_invoice(message, bot)


@bot.message_handler(content_types=['text'])
def check_message(message):
    if message.text.startswith('https://www.youtube.com/') or message.text.startswith('youtube.com/')\
            or message.text.startswith('https://youtu.be/') or message.text.startswith('youtu.be/'):
        bot.send_message(message.chat.id, "Processing...\nIt may take a minute")
        threading.Thread(target=download_audio.download_audio,
                         args=(message.text, message.chat.id, bot)).start()


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                " try to pay again in a few minutes, we need a small rest.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     'Hoooooray! Thanks for payment! We will proceed your order for `{} {}` as fast as possible! '
                     'Stay in touch.\n\nUse /buy again to get a Time Machine for your friend!'.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')


bot.infinity_polling()
