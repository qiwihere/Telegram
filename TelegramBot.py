import requests
import json
import urllib.request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from yandex.Translater import Translater

translater_key = 'trnsl.1.1.20190107T005840Z.04ecacdc7bfd25ac.9026ad4fc123511c3b40305fe406323a9a6c9e0e'
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

tr = Translater()
tr.set_key(translater_key)
tr.set_from_lang('en')
tr.set_to_lang('ru')

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
        tr.set_text(speech_text)
        translated = tr.translate()
        bot.send_message(chat_id=update.message.chat_id, text=translated)


voice_message_handler = MessageHandler(Filters.voice, voiceMessage)

dispatcher.add_handler(voice_message_handler)


# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()