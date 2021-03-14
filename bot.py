from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
from settings import TG_TOKEN
from handlers import *
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def main():
    my_bot = Updater(TG_TOKEN, use_context=True)
    logging.info('Start bot')
    my_bot.dispatcher.add_handler(CommandHandler('start', sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Попугай'), sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Анекдот'), get_anecdote))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.contact, get_contact))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.location, get_location))
    my_bot.dispatcher.add_handler(
        ConversationHandler(entry_points=[MessageHandler(Filters.regex('Анкета'), anketa_start)],
                            states={
                                "user_name": [MessageHandler(Filters.text, anketa_get_name)],
                                "user_subject": [MessageHandler(Filters.text, anketa_get_subject)],
                                "user_points": [MessageHandler(Filters.text,anketa_get_points)],
                                "evaluation": [MessageHandler(Filters.regex('1|2|3|4|5'), anketa_get_evaluation)],
                                "comment": [MessageHandler(Filters.regex('Пропустить'), anketa_exit_comment),
                                            MessageHandler(Filters.text, anketa_comment)]
                            },
                            fallbacks=[MessageHandler(
                                Filters.text | Filters.video | Filters.photo | Filters.document, dontknow)]
                            )
    )

    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))
    my_bot.start_polling()
    my_bot.idle()

if __name__ == '__main__':
    main()
