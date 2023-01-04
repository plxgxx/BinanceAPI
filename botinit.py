import os
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler
from statefuncs import *
from handlers.config_handlers import *
from handlers.stats_handlers import *
from states import *
from data import text


""" inicialise handlers and start the bot """


def main():
    bot_token = os.getenv("BOT_TOKEN")  # variable, because it is neaded on webhook
    updater = Updater(token=bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    necessary_handlers = [CommandHandler('start', start),
                         ]
    conv_handler = ConversationHandler(
        name="conversation",
        entry_points=[CommandHandler("start", start)],
        states={

            States.MAIN_MENU: [
                *necessary_handlers,
                MessageHandler(Filters.regex(text["binance_reg"]), offer_curr_choice),
                MessageHandler(Filters.regex(text["manage_reg"]), starting_setting),
            ],
            States.CURR_GIVING: [
                *necessary_handlers,
                MessageHandler(Filters.regex(text["currency"]), offer_curr_choice),
                MessageHandler(Filters.regex(text["done_reg"]), offer_payment_choice),#Должен быть переход с Done а не с валюты
                MessageHandler(Filters.regex(text["return_reg"]), start)
            ],
            States.PAYMENT_TYPE: [
                *necessary_handlers,
                MessageHandler(Filters.regex(text["payment"]), offer_payment_choice),
                MessageHandler(Filters.regex(text["done_reg"]), offer_amount_selling),  # Должен быть переход с Done а не с валюты
                MessageHandler(Filters.regex(text["return_reg"]), start)
            ],
            States.AMOUNT_SELLING: [
                *necessary_handlers,
                MessageHandler(Filters.regex(text["numbers"]), offer_ammount_buying),
            ],
            States.AMOUNT_BUYING: [
                *necessary_handlers,
                MessageHandler(Filters.regex(text["numbers"]), offer_spread_amount),
            ],
            States.SPREAD_AMOUNT: [
                *necessary_handlers,
                MessageHandler(Filters.regex(text["numbers"]), offer_order_amount),
            ],
            States.ORDER_AMOUNT: [
                *necessary_handlers,
                MessageHandler(Filters.regex(text["numbers"]), offer_deals_amount),
            ],
            States.DEALS_AMOUNT: [
                *necessary_handlers,
                MessageHandler(Filters.regex(text["numbers"]), order_config_naming),
            ],
            States.CONFIG_NAME: [
                *necessary_handlers,
                MessageHandler(Filters.text, completion_message),
            ],
            States.COMPLETE_CREATION: [
                *necessary_handlers,
                MessageHandler(Filters.regex(text["manage_reg"]), starting_setting),
                MessageHandler(Filters.regex(text["return_reg"]), start)
            ],
            States.SETTING_WELCOME: [
                *necessary_handlers,
                MessageHandler(Filters.regex(text["enable_notif_reg"]), notification_text),
                MessageHandler(Filters.regex(text["market_check_reg"]), checking_market),
                MessageHandler(Filters.regex(text["modifying_reg"]), setting_modify),
                MessageHandler(Filters.regex(text["deleting_reg"]), delete_config),
                MessageHandler(Filters.regex(text["return_reg"]), start)
            ],
            States.SETTING_NOTIFICATIONS: [
                *necessary_handlers,
                MessageHandler(Filters.regex(text["manage_reg"]), starting_setting),
                MessageHandler(Filters.regex(text["return_reg"]), start)
            ],
            States.SETTING_CHECK: [
                *necessary_handlers,
                MessageHandler(Filters.regex(text["enable_notif_reg"]), notification_text),
                MessageHandler(Filters.regex(text["double_check_reg"]), checking_market),
                MessageHandler(Filters.regex(text["manage_reg"]), starting_setting),
                MessageHandler(Filters.regex(text["return_reg"]), start)
            ],
            States.SETTING_MODIFY: [
                *necessary_handlers,
                MessageHandler(Filters.regex(text["manage_reg"]), starting_setting),
                MessageHandler(Filters.regex(text["return_reg"]), start)
            ],
            States.SETTING_DELETE: [
                *necessary_handlers,
                MessageHandler(Filters.regex(text["yes_reg"]), succesfull_delete),
                MessageHandler(Filters.regex(text["no_reg"]), starting_setting)

            ]
        },
        fallbacks=[MessageHandler(Filters.regex(text["done_reg"]), done)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
