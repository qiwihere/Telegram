import requests
import json
import urllib.request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


#Получаем IAM Token
folder_id = 'b1g5ijjultbev6ue6u3l'
oauth = 'AQAAAAAhCBSBAATuwXFbrFfLpECUtyfTrytLZFs'
headers = {
    'Content-Type': 'application/json',
}
data = '{"yandexPassportOauthToken": "'+oauth+'"}'
response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', headers=headers, data=data)
IAM_TOKEN = json.loads(response.text)['iamToken']

token = '623317837:AAHwNgxSD9Kbz2Tz2NBKewVhNUGYZXNJ6jg';
updater = Updater(token=token) # Токен API к Telegram
dispatcher = updater.dispatcher


# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=IAM_TOKEN)


def textMessage(bot, update):
    response = 'Получил Ваше сообщение: ' + update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=response)


def voiceMessage(bot, update):
    file = bot.get_file(update.message.voice.file_id)
    path = file.download()

    data = open(path, 'rb').read()
    params = "&".join([
        "topic=general",
        "folderId=%s" % folder_id,
        "lang=ru-RU"
    ])

    url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize/?%s" % params, data=data)
    url.add_header("Authorization", "Bearer %s" % IAM_TOKEN)
    url.add_header("Transfer-Encoding", "chunked")

    responseData = urllib.request.urlopen(url).read().decode('UTF-8')
    decodedData = json.loads(responseData)

    if decodedData.get("error_code") is None:
        bot.send_message(chat_id=update.message.chat_id, text=decodedData.get("result"))


# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
voice_message_handler = MessageHandler(Filters.voice, voiceMessage)


# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
dispatcher.add_handler(voice_message_handler)


# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()