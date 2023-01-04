from telegram import ReplyKeyboardMarkup
from states import *
from statefuncs import start
from data import text


def starting_setting(update, context):
    reply_keyboard = [
        [text["enable_notif"], text["market_check"]],
        [text["modifying"], text["deleting"]],
        [text["return"]]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["starting"], reply_markup=markup)
    return States.SETTING_WELCOME


def notification_text(update, context):
    reply_keyboard = [
        [text["manage"], text["return"]]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["notification"], reply_markup=markup)
    return States.SETTING_NOTIFICATIONS


def checking_market(update, context):
    reply_keyboard = [
        [text["enable_notif"], text["double_check"]],
        [text["manage"], text["return"]]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["checking"], reply_markup=markup)
    return States.SETTING_CHECK


def setting_modify(update, context):
    reply_keyboard = [
        [text["manage"], text["return"]]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["modify"], reply_markup=markup)
    return States.SETTING_MODIFY


def delete_config(update, context):
    reply_keyboard = [
        [text["yes"], text["no"]]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["delete"], reply_markup=markup)
    return States.SETTING_DELETE


def succesfull_delete(update, context):
    update.message.reply_text(text=text["deleted"])
    return start(update, context)
