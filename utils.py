from telegram import ReplyKeyboardMarkup, KeyboardButton

# функция создаёт клавиатуру и её разметку
def get_keyboard():
    contact_button = KeyboardButton('Отправить контакты', request_contact=True)
    location_button = KeyboardButton('Отправить геопозицию', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([['Попугай', 'Анекдот'],
                                       [contact_button, location_button],
                                       ['Анкета']
                                       ], resize_keyboard=True)
    return my_keyboard