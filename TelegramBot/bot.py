import WebhookServer from server
import telebot
import shelve

bot = telebot.TeleBot(config_bot.TOKEN)

@bot.message_handler(commands=['start'])
def bot_main(message):
    #if message.text == '/main':
    #    show_buttons_main(message)
    #if message.text == buttons.CURRENT_ORDERS:
    #    get_orders(message, True)
    #elif message.text == buttons.MY_ORDERS:
    #    get_orders(message)
    #
    #bot.clear_step_handler(message)
    #bot.register_next_step_handler(message, bot_main)
