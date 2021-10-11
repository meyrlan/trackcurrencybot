import telebot
from telebot import types

import config
import responses as R
from binance_class import BinanceAPI

# client = Client(config.binance_api_key, config.binance_api_security)
# print("Logged into Binance account!")

bot = telebot.TeleBot(config.bot_api_key, parse_mode=None)

@bot.message_handler(commands=["get_price"])
def send_get_price(msg):
    word_list = msg.text.split()
    number_of_words = len(word_list)
    if number_of_words != 2:
        bot.send_message(chat_id=msg.chat.id, text=f"Please, enter as: /get_price XXX")
        return
    _binance_obj = BinanceAPI(p_symbol_first=word_list[1], p_symbol_second=word_list[1])
    if not _binance_obj.check_client_build_ok():
        bot.send_message(chat_id=msg.chat.id, text=f"{word_list[1]} is not valid currency!")
        return
    if word_list[1] == config.currency:
        bot.send_message(chat_id=msg.chat.id, text=f"Price of 1 {word_list[1]} in {config.currency}: 1.00")
        return
    bot.send_message(chat_id=msg.chat.id, text=R.sample_responses(word_list[1], config.currency))

@bot.message_handler(commands=["change_my_currency"])
def send_change_my_currency(msg):
    word_list = msg.text.split()
    number_of_words = len(word_list)
    if number_of_words != 2:
        bot.send_message(chat_id=msg.chat.id, text=f"Please, enter as: /change_my_currency XXX")
        return
    _binance_obj = BinanceAPI(p_symbol_first=word_list[1], p_symbol_second=word_list[1])
    if not _binance_obj.check_client_build_ok():
        bot.send_message(chat_id=msg.chat.id, text=f"{word_list[1]} is not valid currency!")
        return
    config.currency = word_list[1]
    bot.send_message(chat_id=msg.chat.id, text=f"Account currency successfully changed to {config.currency}!")

@bot.message_handler(commands=["get_my_currency"])
def send_my_currency(msg):
    bot.send_message(chat_id=msg.chat.id, text=config.currency)

@bot.message_handler(commands=["close"])
def send_close_menu(msg):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(chat_id=msg.chat.id, text="Menu closed!", reply_markup=markup)

@bot.message_handler(commands=["start", "help"])
def send_help_message(msg):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton("/help")
    button2 = types.KeyboardButton("/get_my_currency")
    button3 = types.KeyboardButton("/change_my_currency")
    button4 = types.KeyboardButton("/get_price")
    button5 = types.KeyboardButton("/close")
    markup.add(button1, button2, button3, button4, button5)
    bot.send_message(chat_id=msg.chat.id, text=
                        "/help - get list of functions\n"
                        "/get_my_currency - currency of your account\n"
                        f"/change_my_currency XXX - change my currency from {config.currency} to XXX\n"
                        f"/get_price XXX - get price of XXX in {config.currency}\n"
                        "/close - close menu", reply_markup=markup)

@bot.message_handler()
def other_case(msg):
    bot.reply_to(msg, "No such command!")

def main():
    print("bot is running!")
    bot.polling()
main()