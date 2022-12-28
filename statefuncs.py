from telegram import ReplyKeyboardMarkup
from botinit import MAIN_MENU, CURR_GIVING, PAYMENT_TYPE, \
 AMOUNT_SELLING, AMOUNT_BUYING, SPREAD_AMOUNT, ORDER_AMOUNT, DEALS_AMOUNT, CONFIG_NAME
from telegram.ext import ConversationHandler


def start(update, context):
    text = "Hello World!"
    reply_keyboard = [
        ["Make an offer", "Offer history"],
        ["What this bot can do?", "Help"],
        ["Done"],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)
    return MAIN_MENU


def help(update, context):
    text = """
        /start -> Welcome to the channel
        /help -> Get answers on your questions
        /faq -> What this bot can do?
        """
    chat_id = update.message.chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text=text
    )


def offer_curr_choice(update, context):
    text = "Choose the currency of your offer, " \
           "tap <Done> if your choice is complete"
    reply_keyboard = [
        ["CHF", "SEK", "PLN"],
        ["CZK", "USD", "EUR"],
        ["UAH", "CAD", "GBP"],
        ["Done", "Return to main menu"]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)
    return CURR_GIVING


def offer_payment_choice(update, context):
    text = "Choose the payment method"
    reply_keyboard = [
        ["Revolut", "Wise", "SkrillMoneyBookers"],
        ["Adcash", "ZEN"],
        ["Done", "Return to main menu"]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text, reply_markup=markup)
    return PAYMENT_TYPE


def offer_amount_selling(update, context):
    text = "Insert the amount of currency you sell"
    #reply_keyboard = update.text
    update.message.reply_text(text=text)
    return AMOUNT_SELLING


def offer_ammount_buying(update, context):
    text = "Insert the amount of currency you want to buy"
    #reply_keyboard = update.text
    update.message.reply_text(text=text)
    return AMOUNT_BUYING


def offer_spread_amount(update, context):
    text = "Insert the minimal spread rate"
    #reply_keyboard = update.text
    update.message.reply_text(text=text)
    return SPREAD_AMOUNT


def offer_order_amount(update, context):
    text = "Insert the amount of successful orders"
    #reply_keyboard = update.text
    update.message.reply_text(text=text)
    return ORDER_AMOUNT


def offer_deals_amount(update, context):
    text = "Insert the amount of deals performed"
    #reply_keyboard = update.text
    update.message.reply_text(text=text)
    return DEALS_AMOUNT


def order_config_naming(update, context):
    text = "Give the name to this deal configuration"
    #reply_keyboard = update.text
    update.message.reply_text(text=text)
    return CONFIG_NAME


def done(update, context):
    return ConversationHandler.END


def faq(update, context):
    text = """This bot is capable of making 
    your P2P transactions filter easier"""
    chat_id = update.message.chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text=text
    )
    return MAIN_MENU


