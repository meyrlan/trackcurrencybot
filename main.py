import config
import responses as R
import telebot
from telebot import types
from binance_class import BinanceAPI

from binance.client import Client
import configparser

# client = Client(config.binance_api_key, config.binance_api_security)
# # info = client.get_account()  # Getting account info
# klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MONTH, "1 month ago UTC")
#
# print(klines)

bot = telebot.TeleBot(config.bot_api_key)

@bot.message_handler(commands=["convert"])
def send_get_price(msg):
    word_list = msg.text.split()
    number_of_words = len(word_list)
    if number_of_words != 3:
        bot.send_message(chat_id=msg.chat.id, text=f"Please, enter as: /convert x y")
        return
    _binance_obj = BinanceAPI(p_symbol_first=word_list[1], p_symbol_second=word_list[1])
    if not _binance_obj.check_client_build_ok():
        bot.send_message(chat_id=msg.chat.id, text=f"{word_list[1]} is not valid currency!")
        return
    _binance_obj = BinanceAPI(p_symbol_first=word_list[2], p_symbol_second=word_list[2])
    if not _binance_obj.check_client_build_ok():
        bot.send_message(chat_id=msg.chat.id, text=f"{word_list[2]} is not valid currency!")
        return
    if word_list[1] == word_list[2]:
        bot.send_message(chat_id=msg.chat.id, text=f"{word_list[1]} = {word_list[2]}")
        return
    bot.send_message(chat_id=msg.chat.id, text=R.sample_responses(word_list[1], word_list[2]))

@bot.message_handler(commands=["price"])
def send_get_price(msg):
    word_list = msg.text.split()
    number_of_words = len(word_list)
    if number_of_words != 2:
        bot.send_message(chat_id=msg.chat.id, text=f"Please, enter as: /price x")
        return
    _binance_obj = BinanceAPI(p_symbol_first=word_list[1], p_symbol_second=word_list[1])
    if not _binance_obj.check_client_build_ok():
        bot.send_message(chat_id=msg.chat.id, text=f"{word_list[1]} is not valid currency!")
        return
    if word_list[1] == "USDT":
        bot.send_message(chat_id=msg.chat.id, text=f"{word_list[1]} = USDT")
        return
    bot.send_message(chat_id=msg.chat.id, text=R.sample_responses(word_list[1], "USDT"))

@bot.message_handler(commands=["close"])
def send_close_menu(msg):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(chat_id=msg.chat.id, text="Menu closed!")

@bot.message_handler(commands=["start", "help"])
def send_help_message(msg):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton("/help")
    button2 = types.KeyboardButton("/convert")
    button3 = types.KeyboardButton("/price")
    button4 = types.KeyboardButton("/close")
    markup.add(button1, button2, button3, button4)
    bot.send_message(chat_id=msg.chat.id, text=
                        "/help - list options\n/convert x y - convert from x to y \n/price x - price of x in USDT \n/close - close menu", reply_markup=markup)

@bot.message_handler()
def other_case(msg):
    bot.reply_to(msg, "No such command!")

def main():
    print("bot is running!")
    bot.polling()
main()