
# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
updater = Updater(token='623317837:AAHwNgxSD9Kbz2Tz2NBKewVhNUGYZXNJ6jg')  # Токен API к Telegram
dispatcher = updater.dispatcher


# Обработка команд
def start_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')


def text_message(bot, update):
    response = 'Получил Ваше сообщение: ' + update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=response)

def voice_message(bot, update):
    response = 'Audio: ' + update.message.voice.file_id
    bot.send_message(chat_id=update.message.chat_id, text=response)


# Хендлеры
start_command_handler = CommandHandler('start', start_command)
text_message_handler = MessageHandler(Filters.text, text_message)
voice_mesage_handler = MessageHandler(Filters.voice, voice_message)

# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
dispatcher.add_handler(voice_mesage_handler)

# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
