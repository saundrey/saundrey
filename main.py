import telebot
from telebot import types
import config
from telebot.types import LabeledPrice, ShippingOption

bot = telebot.TeleBot(config.BOT_TOKEN)
provider_token = '381764678:TEST:80296'
prices = [LabeledPrice(label='Working Time Machine', amount=5750), LabeledPrice('Gift wrapping', 500)]

shipping_options = [
    ShippingOption(id='instant', title='WorldWide Teleporter').add_price(LabeledPrice('Teleporter', 1000)),
    ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Pickup', 300))]

@bot.message_handler(commands=["start"],)
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu = types.KeyboardButton(text='/menu')
    raspisanie = types.KeyboardButton(text="/расписание")
    markup.add(menu, raspisanie)
    bot.send_message(message.chat.id, "привет, нажми на одну из кнопок ", reply_markup=markup)

@bot.message_handler(commands=["menu"])
def menu(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text='да', callback_data="yes")
    item_no = types.InlineKeyboardButton(text='нет', callback_data="no")
    markup_inline.add(item_yes, item_no)
    bot.send_message(message.chat.id, "вы хотите увидеть меню?", reply_markup=markup_inline)

@bot.message_handler(commands=["расписание"])
def raspisanie(message):
    file3 = open("расписание.jpeg", 'rb')
    bot.send_photo(message.chat.id,file3, "график работы столовой", )
@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'yes':
        markup_reply = types.InlineKeyboardMarkup()
        item_bludo1 = types.InlineKeyboardButton(text='блюдо 1', callback_data="блюдо 1")
        item_bludo2 = types.InlineKeyboardButton(text='блюдо 2', callback_data="блюдо 2")
        markup_reply.add(item_bludo1, item_bludo2)
        file = open('меню.jpg', 'rb')
        bot.send_photo(call.message.chat.id, file, 'выберите позицию из меню нажав на одну из кнопок',
                       reply_markup=markup_reply)
    elif call.data == "no":
        pass
    elif call.data == "zakaz":
        markup_inline_oplata = types.InlineKeyboardMarkup()
        card = types.InlineKeyboardButton(text='наличными на кассе', callback_data="cash")
        cash = types.InlineKeyboardButton(text='картой', callback_data="card")
        markup_inline_oplata.add(cash, card)
        file2 = open('деньги.png', 'rb')
        bot.send_photo(call.message.chat.id, file2, 'как бы вы хотели оплатить заказ',
                       reply_markup=markup_inline_oplata)
    elif call.data == "otmena":
        pass
    elif call.data == "cash":
        markup_inline_time = types.InlineKeyboardMarkup()
        time1 = types.InlineKeyboardButton(text="10:00-10:30", callback_data='time')
        time2 = types.InlineKeyboardButton(text="10:30-11:00", callback_data='time')
        time3 = types.InlineKeyboardButton(text="11:30-12:00", callback_data='time')
        time4 = types.InlineKeyboardButton(text="12:00-12:30", callback_data='time')
        time5 = types.InlineKeyboardButton(text="13:00-13:30", callback_data='time')
        time6 = types.InlineKeyboardButton(text="14:00-14:30", callback_data='time')
        markup_inline_time.add(time6, time1, time5, time4, time3, time2)
        bot.send_message(call.message.chat.id, 'Во сколько вам удобно забрать заказ?', reply_markup=markup_inline_time)
    elif call.data == 'time':
        bot.send_message(call.message.chat.id, "Ваш заказ оформлен, спасибо")
    elif call.data == "блюдо 1":
        markup_inline = types.InlineKeyboardMarkup()
        item_da = types.InlineKeyboardButton(text='да', callback_data="zakaz")
        item_net = types.InlineKeyboardButton(text='нет', callback_data="otmena")
        markup_inline.add(item_da, item_net)
        bot.send_message(call.message.chat.id, 'вы заказали стейк, перейти к оформлению заказа?',
                         reply_markup=markup_inline)
    elif call.data == "блюдо 2":
        markup_inline = types.InlineKeyboardMarkup()
        item_da = types.InlineKeyboardButton(text='да', callback_data="zakaz")
        item_net = types.InlineKeyboardButton(text='нет', callback_data="otmena")
        markup_inline.add(item_da, item_net)
        bot.send_message(call.message.chat.id, 'вы заказали рыбу, перейти к оформлению заказа?',
                         reply_markup=markup_inline)

    elif call.data == "card" :
        bot.send_invoice(
            call.message.chat.id,  # chat_id
            'блюдо',  # title
            'оплатите пожалуйста свою порцию',
            # description
            'HAPPY FRIDAYS COUPON',  # invoice_payload
            provider_token,  # provider_token
            'rub',  # currency
            prices,  # prices
            photo_url='https://avatars.mds.yandex.net/i?id=3c59b0dfe58c010c003c0cb0081f40919b115e1b-12612451-images-thumbs&n=13',
            photo_height=512,  # !=0/None or picture won't be shown
            photo_width=512,
            photo_size=512,
            is_flexible=False,  # True If you need to set up Shipping Fee
            start_parameter='time-machine-example')

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                " try to pay again in a few minutes, we need a small rest.")

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    markup_inline_time=types.InlineKeyboardMarkup()
    time1 = types.InlineKeyboardButton(text="10:00-10:30", callback_data='time')
    time2 = types.InlineKeyboardButton(text="10:30-11:00", callback_data='time')
    time3 = types.InlineKeyboardButton(text="11:30-12:00", callback_data='time')
    time4 = types.InlineKeyboardButton(text="12:00-12:30", callback_data='time')
    time5 = types.InlineKeyboardButton(text="13:00-13:30", callback_data='time')
    time6 = types.InlineKeyboardButton(text="14:00-14:30", callback_data='time')
    markup_inline_time.add(time6, time1, time5, time4, time3, time2)
    bot.send_message(message.chat.id,
                     'отлчно,оплата прошла успешно'.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')
    bot.send_message(message.chat.id, 'Во сколько вам удобно забрать заказ?', reply_markup=markup_inline_time)
bot.polling(none_stop=True,interval=0)
