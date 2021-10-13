import config
import responses as R
import telebot
from telebot import types
from binance_class import BinanceAPI

bot = telebot.TeleBot(config.bot_api_key, parse_mode=None)

@bot.message_handler(commands=["gp"])
def send_get_price(msg):
    word_list = msg.text.split()
    number_of_words = len(word_list)
    if number_of_words != 2:
        bot.send_message(chat_id=msg.chat.id, text=f"Please, enter as: /gp XXX")
        return
    _binance_obj = BinanceAPI(p_symbol_first=word_list[1], p_symbol_second=word_list[1])
    if not _binance_obj.check_client_build_ok():
        bot.send_message(chat_id=msg.chat.id, text=f"{word_list[1]} is not valid currency!")
        return
    if word_list[1] == config.currency:
        bot.send_message(chat_id=msg.chat.id, text=f"{word_list[1]} = {config.currency}")
        return
    bot.send_message(chat_id=msg.chat.id, text=R.sample_responses(word_list[1], config.currency))

@bot.message_handler(commands=["cmc"])
def send_change_my_currency(msg):
    word_list = msg.text.split()
    number_of_words = len(word_list)
    if number_of_words != 2:
        bot.send_message(chat_id=msg.chat.id, text=f"Please, enter as: /cmc XXX")
        return
    _binance_obj = BinanceAPI(p_symbol_first=word_list[1], p_symbol_second=word_list[1])
    if not _binance_obj.check_client_build_ok():
        bot.send_message(chat_id=msg.chat.id, text=f"{word_list[1]} is not valid currency!")
        return
    config.currency = word_list[1]
    bot.send_message(chat_id=msg.chat.id, text=f"Account currency changed to {config.currency}!")

@bot.message_handler(commands=["gmc"])
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
    button2 = types.KeyboardButton("/gmc")
    button3 = types.KeyboardButton("/cmc")
    button4 = types.KeyboardButton("/gp")
    button5 = types.KeyboardButton("/close")
    markup.add(button1, button2, button3, button4, button5)
    bot.send_message(chat_id=msg.chat.id, text=
                        "/help - list options\n/gmc - currency of your account\n/cmc XXX - change my currency from BTC to XXX\n/gp XXX - get price of XXX in BTC\n/close - close menu", reply_markup=markup)

@bot.message_handler()
def other_case(msg):
    bot.reply_to(msg, "No such command!")

def main():
    print("bot is running!")
    bot.polling()
main()