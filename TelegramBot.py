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

    #if decodedData.get("error_code") is None:
    #    bot.send_message(chat_id=update.message.chat_id, text=decodedData.get('result'))
    if decodedData.get("error_code") is None:
        speech_text = decodedData.get('result')
        params = "&".join([
            "text=$s" % speech_text,
            "target=en"
            "folderId=%s" % folder_id,

        ])

        url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize/?%s" % params)
        url.add_header("Authorization", "Bearer %s" % IAM_TOKEN)

        responseData = urllib.request.urlopen(url).read().decode('UTF-8')
        bot.send_message(chat_id=update.message.chat_id, text=responseData)
        # decodedData = json.loads(responseData)



voice_message_handler = MessageHandler(Filters.voice, voiceMessage)

dispatcher.add_handler(voice_message_handler)


# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()