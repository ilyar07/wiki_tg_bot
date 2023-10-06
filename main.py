from telebot import *
from config import *
import wikipedia as wiki
import re
import datetime


bot = TeleBot(TOKEN)


def request2wiki(message: types.Message, save_file: str = 'requests.txt') -> str:
    """Делает запрос на википедию записывает информацию запроса в файл (save_file) и возвращает кратокое содержание"""

    pattern = re.compile('[а-яА-Я]')
    name_page = message.text
    lang = 'ru' if re.search(pattern, name_page) else 'en'
    wiki.set_lang(lang)

    with open(save_file, 'at', encoding='utf-8') as f:
        f.write(
            f'REQUEST {datetime.now()}:\nContent: {repr(name_page)}\nUser: {message.chat.first_name} {message.chat.last_name}.\n\n')

    try:
        page = wiki.summary(name_page)

    except wiki.exceptions.DisambiguationError:
        return 'Пожалуйста уточните запрос' if lang == 'ru' else 'Please refine request'

    except wiki.exceptions.PageError:
        return 'Я такого не нашел(' if lang == 'ru' else 'I didn`t find that('

    return page


@bot.message_handler(commands=['start', 'help'])
def start_message(message: types.Message) -> None:
    """Приветсвие"""

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Сообщить об ошибке ⛔' if message.from_user.language_code == 'ru' else 'Report a bug ⛔')
    markup.add(btn1)
    bot.send_message(message.chat.id, 'Привет, ты можешь спросить у меня\n'
                                      'любое определение' if message.from_user.language_code == 'ru' else 'Hi, you can ask me\n'
                                                                                                          'any definition', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text_hangler(message: types.Message) -> None:
    """Обработка текста"""

    if message.text == 'Сообщить об ошибке ⛔':
        bot.send_message(message.chat.id, 'Опишите вашу проблему сюда - @rotgan1\nзаранее спасибо за помощь!')

    elif message.text == 'Report a bug ⛔':
        bot.send_message(message.chat.id, 'Describe your problem here - @rotgan1\nthanks in advance for your help!')

    else:
        response = request2wiki(message)
        bot.send_message(message.chat.id, response)


def main():
    print('Bot started...')
    bot.infinity_polling()


if __name__ == '__main__':
    main()
