import os
import sys
import logging
from telegram.ext import Updater, Filters, PicklePersistence
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from statefuncs import *
from handlers.config_handlers import *
from handlers.stats_handlers import *
from states import *
from data import text
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

print("-------- succesful import --------")


""" inicialise handlers and start the bot """


def error_handler(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    storage_file = "storage"
    my_persistence = PicklePersistence(filename=storage_file)

    bot_token = os.getenv("BOT_TOKEN")  # variable, because it is neaded on webhook
    updater = Updater(token=bot_token, use_context=True, persistence=my_persistence)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    if ("--service" in sys.argv) or ("-s" in sys.argv):
        print("!!!!!!!! bot on service !!!!!!!!")
        dispatcher.add_handler(MessageHandler((Filters.text | Filters.command), echo_service))
    else:
        necessary_handlers = [CommandHandler('start', start),
                              CommandHandler('faq', faq),
                            ]
        conv_handler = ConversationHandler(
            name="conversation",
            persistent=True,
            entry_points=necessary_handlers,
            states={

            States.MAIN_MENU: [
                *necessary_handlers,
                MessageHandler(Filters.text([text["binance"]]), offer_curr_choice),
                MessageHandler(Filters.text([text["manage"]]), config_choice),
            ],
            States.PASSWORD_CHECK: [
                *necessary_handlers,
                MessageHandler(Filters.text, password_check),
            ],
            States.NAME_AND_SURNAME: [
                *necessary_handlers,
                MessageHandler(Filters.text, get_name_surname)
            ],
            States.CURR_GIVING: [
                *necessary_handlers,
                MessageHandler(Filters.regex(text["currency"]), offer_payment_choice),
                MessageHandler(Filters.text([text["return"]]), start)
            ],
            States.PAYMENT_TYPE: [
                *necessary_handlers,
                CallbackQueryHandler(offer_payment_choice, pass_chat_data=True, pass_user_data=True),
                MessageHandler(Filters.text([text["return"]]), start)
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
                MessageHandler(Filters.text([text["manage"]]), config_choice),
                MessageHandler(Filters.text([text["return"]]), start),
            ],
            States.SETTING_CHOICE:[
               *necessary_handlers,
                MessageHandler(Filters.text([text["return"]]), start),
                MessageHandler(Filters.text, starting_setting),
            ],
            States.SETTING_WELCOME: [
                *necessary_handlers,
                MessageHandler(Filters.text([text["enable_notif"]]), notification_text),
                MessageHandler(Filters.text([text["market_check"]]), checking_market),
                MessageHandler(Filters.text([text["modifying"]]), setting_modify),
                MessageHandler(Filters.text([text["deleting"]]), delete_config),
                MessageHandler(Filters.text([text["return"]]), start)
            ],
            States.SETTING_NOTIFICATIONS: [
                *necessary_handlers,
                MessageHandler(Filters.text([text["manage"]]), starting_setting),
                MessageHandler(Filters.text([text["return"]]), start)
            ],
            States.SETTING_CHECK: [
                *necessary_handlers,
                MessageHandler(Filters.text([text["enable_notif"]]), notification_text),
                MessageHandler(Filters.text([text["double_check"]]), checking_market),
                MessageHandler(Filters.text([text["manage"]]), starting_setting),
                MessageHandler(Filters.text([text["return"]]), start)
            ],
            States.SETTING_MODIFY: [
                *necessary_handlers,
                MessageHandler(Filters.text([text["manage"]]), starting_setting),
                MessageHandler(Filters.text([text["name"]]), modify_name),
                MessageHandler(Filters.text([text["volume_b"]]),  modify_name),
                MessageHandler(Filters.text([text["volume_s"]]),  modify_name),
                MessageHandler(Filters.text([text["payment_c"]]),  modify_name),
                MessageHandler(Filters.text([text["%orders"]]),  modify_name),
                MessageHandler(Filters.text([text["deals"]]),  modify_name),
                MessageHandler(Filters.text([text["%spread"]]),  modify_name),
                MessageHandler(Filters.text([text["return"]]), start)
            ],
            States.SETTING_DELETE: [
                *necessary_handlers,
                MessageHandler(Filters.regex(text["yes_reg"]), succesfull_delete),
                MessageHandler(Filters.regex(text["no_reg"]), starting_setting)

            ],
            States.MODIFY_NAME:[
                *necessary_handlers,
                MessageHandler(Filters.text(text["return"]), start),
                MessageHandler(Filters.text, modify_name_complete)
            ],
            States.MODIFY_BUY:[],
            States.MODIFY_SELL:[],
            States.MODIFY_PAYMENT:[],
            States.MODIFY_ORDERS:[],
            States.MODIFY_DEALS:[],
            States.MODIFY_SPREAD:[]
        },
        fallbacks=[CommandHandler('stop', done)],
    )

        dispatcher.add_handler(conv_handler)
    

    dispatcher.add_error_handler(error_handler)


    if ("--web-hook" in sys.argv) or ("-w" in sys.argv):
        print("-------- starting webhook --------")
        host_port = int(os.getenv("WEBHOOK_PORT"))
        host_url = os.getenv("WEBHOOK_URL")
        webhook_host_url = f"https://{host_url}:{host_port}/{bot_token}"
        print("started on\n\n" + webhook_host_url)
        updater.start_webhook(
            listen="0.0.0.0",
            port=host_port,
            url_path=bot_token,
            key="private.key",
            cert="cert.pem",
            webhook_url=webhook_host_url,
        )
    else:
        print("-------- starting polling --------")
        updater.start_polling()

    
    updater.idle()


if __name__ == '__main__':
    main()
