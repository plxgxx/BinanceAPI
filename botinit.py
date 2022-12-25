import os
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler
from statefuncs import *

""" inicialise handlers and start the bot """

MAIN_MENU, CURR_GIVING, CRYPT_RECIEVING = range(3)



def main():
    bot_token = os.getenv("BOT_TOKEN")  # variable, because it is neaded on webhook
    updater = Updater(token=bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    necessary_handlers = [CommandHandler('start', start),
                          CommandHandler('help', help),
                          CommandHandler('faq', faq)]
    conv_handler = ConversationHandler(
        name="conversation",
        entry_points=[CommandHandler("start", start)],
        states={

            MAIN_MENU: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^Make an offer$"), offer_curr_choice),
               # MessageHandler(Filters.regex("^Offer history$"), offer_history),
                MessageHandler(Filters.regex("^What this bot can do?"), faq),
                MessageHandler(Filters.regex("^Help$"), help)
            ],
            CURR_GIVING: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^CHF|SEK|PLN|CZK|USD|EUR|UAH|CAD|GBP"), offer_crypt_choice),
            ]

        },
        fallbacks=[MessageHandler(Filters.regex("^Done$"), done)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()






if __name__ == '__main__':
    main()
