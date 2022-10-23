from telebot.types import LabeledPrice

PT = "401643678:TEST:813fabf7-13fc-4b23-b2e7-82078deb80bc"

prices = [LabeledPrice(label="Subscription", amount=1000)]


def send_invoice(message, bot):
    print("in send")
    bot.send_invoice(
        message.chat.id,  # chat_id
        'Subscription',  # title
        'Subscription for 1 month',  # description
        'HAPPY FRIDAYS COUPON',  # invoice_payload
        PT,  # provider_token
        'rub',  # currency
        prices,  # prices
        photo_url='1.png',
        photo_height=512,  # !=0/None or picture won't be shown
        photo_width=512,
        photo_size=512,
        is_flexible=False,  # True If you need to set up Shipping Fee
        start_parameter='time-machine-example')



