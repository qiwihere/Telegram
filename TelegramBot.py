from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot
updater = Updater(token='623317837:AAHwNgxSD9Kbz2Tz2NBKewVhNUGYZXNJ6jg')
dispatcher = updater.dispatcher



# Обработка команд для бота телеги лол
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')

def textMessage(bot, update):
    response = 'Получил Ваше сообщение: ' + update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=response)

# Хендлеры
start_command_handler = CommandHandler('start', startCommand)

text_message_handler = MessageHandler(Filters.text, textMessage)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()