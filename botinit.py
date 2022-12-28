import os
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler
from statefuncs import *

""" inicialise handlers and start the bot """

MAIN_MENU, CURR_GIVING, PAYMENT_TYPE, AMOUNT_SELLING, \
 AMOUNT_BUYING, SPREAD_AMOUNT, ORDER_AMOUNT, DEALS_AMOUNT, CONFIG_NAME = range(9)



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
                MessageHandler(Filters.regex("^CHF|SEK|PLN|CZK|USD|EUR|UAH|CAD|GBP"), offer_curr_choice),
                MessageHandler(Filters.regex("^Done$"), offer_payment_choice),#Должен быть переход с Done а не с валюты
                MessageHandler(Filters.regex("^Return to main menu$"), start)
            ],
            PAYMENT_TYPE: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^Revolut|Wise|SkrillMoneyBookers|Adcash|ZEN"), offer_payment_choice),
                MessageHandler(Filters.regex("^Done$"), offer_amount_selling),  # Должен быть переход с Done а не с валюты
                MessageHandler(Filters.regex("^Return to main menu$"), start)
            ],
            AMOUNT_SELLING: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^[0-9]"), offer_ammount_buying),
            ],
            AMOUNT_BUYING: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^[0-9]"), offer_spread_amount),
            ],
            SPREAD_AMOUNT: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^[0-9]"), offer_order_amount),
            ],
            ORDER_AMOUNT: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^[0-9]"), offer_deals_amount),
            ],
            DEALS_AMOUNT: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^[0-9]"), order_config_naming),
            ],
            CONFIG_NAME: [
                *necessary_handlers,
                MessageHandler(Filters.text, start),
            ]

        },
        fallbacks=[MessageHandler(Filters.regex("^Done$"), done)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
