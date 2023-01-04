import os
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler
from statefuncs import *
from handlers.config_handlers import *
from handlers.stats_handlers import *
from states import *


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
                MessageHandler(Filters.regex("^Binance P2P$"), offer_curr_choice),
                MessageHandler(Filters.regex("^Hастроить конфиг$"), starting_setting),
            ],
            States.CURR_GIVING: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^CHF|SEK|PLN|CZK|USD|EUR|UAH|CAD|GBP"), offer_curr_choice),
                MessageHandler(Filters.regex("^Готово"), offer_payment_choice),#Должен быть переход с Done а не с валюты
                MessageHandler(Filters.regex("^Return to main menu$"), start)
            ],
            States.PAYMENT_TYPE: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^Revolut|Wise|SkrillMoneyBookers|Adcash|ZEN"), offer_payment_choice),
                MessageHandler(Filters.regex("^Готово"), offer_amount_selling),  # Должен быть переход с Done а не с валюты
                MessageHandler(Filters.regex("^Return to main menu$"), start)
            ],
            States.AMOUNT_SELLING: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^[0-9]"), offer_ammount_buying),
            ],
            States.AMOUNT_BUYING: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^[0-9]"), offer_spread_amount),
            ],
            States.SPREAD_AMOUNT: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^[0-9]"), offer_order_amount),
            ],
            States.ORDER_AMOUNT: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^[0-9]"), offer_deals_amount),
            ],
            States.DEALS_AMOUNT: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^[0-9]"), order_config_naming),
            ],
            States.CONFIG_NAME: [
                *necessary_handlers,
                MessageHandler(Filters.text, completion_message),
            ],
            States.COMPLETE_CREATION: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^Настроить конфигурацию"), starting_setting),
                MessageHandler(Filters.regex("^Вернуться в главное меню"), start)
            ],
            States.SETTING_WELCOME: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^Включить уведомления"), notification_text),
                MessageHandler(Filters.regex("^Проверить сейчас"), checking_market),
                MessageHandler(Filters.regex("^Редактировать"), setting_modify),
                MessageHandler(Filters.regex("^Удалить"), delete_config),
                MessageHandler(Filters.regex("^Вернуться в главное меню"), start)
            ],
            States.SETTING_NOTIFICATIONS: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^Настроить конфигурацию"), starting_setting),
                MessageHandler(Filters.regex("^Вернуться в главное меню"), start)
            ],
            States.SETTING_CHECK: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^Включить уведомления"), notification_text),
                MessageHandler(Filters.regex("^Проверить ещё раз"), checking_market),
                MessageHandler(Filters.regex("^В настройки конфигурации"), starting_setting),
                MessageHandler(Filters.regex("^Вернуться в главное меню"), start)
            ],
            States.SETTING_MODIFY: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^В настройки конфигурации"), starting_setting),
                MessageHandler(Filters.regex("^Вернуться в главное меню"), start)
            ],
            States.SETTING_DELETE: [
                *necessary_handlers,
                MessageHandler(Filters.regex("^Да"), succesfull_delete),
                MessageHandler(Filters.regex("^Нет"), starting_setting)

            ]
        },
        fallbacks=[MessageHandler(Filters.regex("^Готово$"), done)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
