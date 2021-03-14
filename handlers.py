from bs4 import BeautifulSoup
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup, ParseMode
from mongodb import mdb, search_or_save_user, save_user_anketa
from utils import get_keyboard
import requests


def sms(bot, update):  # используется при команде start
    user = search_or_save_user(mdb, bot.effective_user, bot.message)
    print(user)
    print('Кто-то отправил команду /start что мне делать?')
    bot.message.reply_text('Привет, {}! \nМеня зовут ПостуБот)'
                           .format(bot.message.chat.first_name), reply_markup=get_keyboard())
    print(bot.message)


def get_anecdote(bot, update):
    receive = requests.get('http://anekdotme.ru/random')
    page = BeautifulSoup(receive.text, "html.parser")
    find = page.select('.anekdot_text')
    for text in find:
        page = (text.getText().strip())
    bot.message.reply_text(page)


def parrot(bot, update):  # отвечает за работу бота попугаем
    print(bot.message.text)
    bot.message.reply_text(bot.message.text)


def get_contact(bot, update):
    print(bot.message.location)
    bot.message.reply_text('{}, мы получили ваш номер  телефона'.format(bot.message.chat.first_name))


def get_location(bot, update):
    print(bot.message.location)
    bot.message.reply_text('{}, мы получили ваше местоположение'.format(bot.message.chat.first_name))


def anketa_start(bot, update):
    user = search_or_save_user(mdb, bot.effective_user, bot.message)
    if 'anketa' in user:
        text = """Ваш предыдущий результат:
         <b>Имя:</b> {name}
    <b>Возраст:</b> {age}
    <b>Оценка:</b> {evaluation}
    <b>Комментарий</b> {comment}

Данные будут обновлены! 
         Как вас зовут?""".format(**user['anketa'])
        bot.message.reply_text(
            text, parse_mode=ParseMode.HTML)
        return "user_name"
    else:
        bot.message.reply_text('Как вас зовут?')
        return "user_name"

    bot.message.reply_text('Как вас зовут?')  # вопрос
    return "user_name"  # ключ для опреденелия следующего шага


def anketa_get_name(bot, update):
    update.user_data['name'] = bot.message.text  # временно сохраняем ответы
    bot.message.reply_text("Какие дополнительные предматы вы сдаёте на ЕГЭ?")  # задаём вопрос
    return "user_subject"  # ключ для определения следующего шага


def anketa_get_subject(bot, update):
    update.user_data['subject'] = bot.message.text
    bot.message.reply_text('Сколько у вас баллов?')
    return "user_points"


def anketa_get_points(bot, update):
    update.user_data['subject'] = bot.message.text
    reply_keyboard = [["1", "2", "3", "4", "5"]]  # создаём клавиатуру
    bot.message.reply_text(
        "Оцените мою работу от 1 до 5",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                         one_time_keyboard=True))  # при нажати клавиатура исчезает
    return "evaluation"


def anketa_get_evaluation(bot, update):
    update.user_data['evaluation'] = bot.message.text
    reply_keyboard = [['Пропустить']]
    bot.message.reply_text("Оставьте отзыв или нажмите пропустить этот шаг",
                           reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                            one_time_keyboard=True))
    return "comment"


def anketa_comment(bot, update):
    update.user_data['comment'] = bot.message.text
    user = search_or_save_user(mdb, bot.effective_user, bot.message)
    anketa = save_user_anketa(mdb, user, update.user_data)
    print(anketa)
    text = """Результат опроса:
    <b>Имя:</b> {name}
    <b>Дополнительные предметы:</b> {subject}
    <b>Баллы за ЕГЭ:</b> {points}
    <b>Оценка:</b> {evaluation}
    <b>Комментарий</b> {comment}
    """.format(**update.user_data)
    bot.message.reply_text(text, parse_mode=ParseMode.HTML)  # текстовое сообщение в формате HTML
    bot.message.reply_text("Спасибо вам за комментарий",
                           reply_markup=get_keyboard())  # отправляет сообщение и возвращает оьмновную клавиатуру
    return ConversationHandler.END


def anketa_exit_comment(bot, update):
    update.user_data['comment'] = None
    user = search_or_save_user(mdb, bot.effective_user, bot.message)
    save_user_anketa(mdb, user, update.user_data)
    text = """Результат опроса:
    <b>Дополнительные предметы:</b> {subject}
    <b>Баллы за ЕГЭ:</b> {points}
    <b>Оценка:</b> {evaluation} """.format(**update.user_data)
    bot.message.reply_text(text, parse_mode=ParseMode.HTML)
    bot.message.reply_text("Спасибо!", reply_markup=get_keyboard())
    return ConversationHandler.END


def dontknow(bot):
    bot.message.reply_text("Я вас не понимаю, выберете оценку на клавиатуре!")
