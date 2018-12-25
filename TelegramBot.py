
# Настройки
import urllib.request
import urllib.parse
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

IAM_TOKEN = 'CggaATEVAgAAABKABBCEyfz6JOU8lplxvnZSwsSvtI8vvCEhwlri1l7QEOR04MWlGf1B3Dns_csgXo1ijuTDfaSN2bKigm0_4Pk5UhD_U9Z8hSyMj06n3zUWPG5znAhqJKri17-4avRrWivptS0J47IHSGHeBWf56IvCpPCPQYg8NRGswPs0oksqKz_c05UEHPh5EdPm9dSTUrKTi1ZwwNh2SmME4Qh6elt-Qptao_rE5EezvwDnlE6mP_pfZZyfx1QRivi4UajsIMYDNzC0WG17nptCaAeUFl94iTjGunfWNspraZH-Z5ty1aGsSwmrDhKXik637T2jtrp9nnH-X5kCfr7Bt3p6xfVxM5e7J4O_AFp-3X5rBVzqXOicfYfMt3WwY9ThK637ggrI5oPYyGLdNF0ys8_flO8238jrqUwTAL5529N1h6XrxFUdtyyi8nzEqUwegpJAIJyg1IofyC2XjvzdN_UiS7uBRGnVnl5koPQBas7m37a3LCxJzqNBn_BQw7r6dIPJZ6fDUWtmK5LzS6fZinBHCPmzFRFsHBg_23UBGEk4LwN2OjbuDI2Rkyw2AsCTC4WuJUxyrQJTr7R3hXdepOxTcXukYx_zseUd5gzNn_Cnh3J6TCYfVkpbhgFTZciplv-JHu6TR4kmBpMpLKifPD_jEKgfkAGFCKWcXmETixjsiC2ox0hQGmYKIDk5Yzg3YWExMjAxMDRjZmJhMTU0ZDhkNTk2YzI0MjhhENfliuEFGJe3jeEFIiQKFGFqZWJtbzNpODdnMG0yYTJhODJqEgxhcnRlbWxpcG92b3laADACOAFKCBoBMRUCAAAAUAEg9QQ"'
FOLDER_ID = 'b1g5ijjultbev6ue6u3l'

'''
OAuthToken = 'AQAAAAAhCBSBAATuwXFbrFfLpECUtyfTrytLZFs'


params = {'yandexPassportOauthToken': OAuthToken}

url = urllib.request.Request("https://iam.api.cloud.yandex.net/iam/v1/tokens", data=urllib.parse.urlencode(params).encode("utf-8"))
url.add_header("User-Agent", "AppleWebKit/537.36 (KHTML, like Gecko)")
url.add_header("Content-Type", "application/json")
responseData = urllib.request.urlopen(url).read()
decodedData = json.loads(responseData)
'''


updater = Updater(token='623317837:AAHwNgxSD9Kbz2Tz2NBKewVhNUGYZXNJ6jg')  # Токен API к Telegram
dispatcher = updater.dispatcher


# Обработка команд
def start_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')


def text_message(bot, update):
    response = 'Получил Ваше сообщение: ' + update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=response)


def voice_message(bot, update):
    file = bot.getFile(update.message.voice.file_id)
    data = file.read()

    params = "&".join([
        "topic=general",
        "folderId=%s" % FOLDER_ID,
        "lang=ru-RU"
    ])

    url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize/?%s" % params, data=data)
    url.add_header("Authorization", "Bearer %s" % IAM_TOKEN)
    url.add_header("Transfer-Encoding", "chunked")

    response_data = urllib.request.urlopen(url).read().decode('UTF-8')
    decoded_data = json.loads(response_data)

    if decoded_data.get("error_code") is None:
        response = 'Answer: ' + decoded_data.get("result")
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text=decoded_data.get("error_code"))


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
