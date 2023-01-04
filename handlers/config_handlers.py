from telegram import ReplyKeyboardMarkup
from states import *
from data import text


def offer_curr_choice(update, context):
    reply_keyboard = [
        ["CHF", "SEK", "PLN"],
        ["CZK", "USD", "EUR"],
        ["UAH", "CAD", "GBP"],
        [text["done"], text["return"]]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["offer_curr_choice"], reply_markup=markup)
    return States.CURR_GIVING


def offer_payment_choice(update, context):
    reply_keyboard = [
        ["Revolut", "Wise", "SkrillMoneyBookers"],
        ["Adcash", "ZEN"],
        [text["done"], text["return"]]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["offer_payment_choice"], reply_markup=markup)
    return States.PAYMENT_TYPE


def offer_amount_selling(update, context):
    #reply_keyboard = update.text
    update.message.reply_text(text=text["offer_amount_selling"])
    return States.AMOUNT_SELLING


def offer_ammount_buying(update, context):
    #reply_keyboard = update.text
    update.message.reply_text(text=text["offer_ammount_buying"])
    return States.AMOUNT_BUYING


def offer_spread_amount(update, context):
    #reply_keyboard = update.text
    update.message.reply_text(text=text["offer_spread_amount"])
    return States.SPREAD_AMOUNT


def offer_order_amount(update, context):
    #reply_keyboard = update.text
    update.message.reply_text(text=text["offer_order_amount"])
    return States.ORDER_AMOUNT


def offer_deals_amount(update, context):
    #reply_keyboard = update.text
    update.message.reply_text(text=text["offer_deals_amount"])
    return States.DEALS_AMOUNT


def order_config_naming(update, context):
    #reply_keyboard = update.text
    update.message.reply_text(text=text["order_config_naming"])
    return States.CONFIG_NAME

def completion_message(update, context):
    reply_keyboard = [
        [text["manage"], text["return"]]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["completion_message"], reply_markup=markup)
    return States.COMPLETE_CREATION
