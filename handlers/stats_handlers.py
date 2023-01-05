from telegram import ReplyKeyboardMarkup

import states
from states import *
from statefuncs import start
from data import text
from database import db_session

def config_choice(update, context):
    chat_id = update.message.chat.id
    choices = db_session.get_configs_list(chat_id)
    print(choices)
    reply_keyboard = [[i[0]]
        for i in choices
    ]
    reply_keyboard.append([text["return"]])
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["choose_config"], reply_markup=markup)
    return States.SETTING_CHOICE


def starting_setting(update, context):
    msg = update.message.text
    config_info = db_session.get_config_info(msg)
    message_text = f"""
    Название: {config_info.name}\n
    
    Объём покупки: {config_info.buy_volume} {config_info.currency}\n
    Объём продажи: {config_info.sale_volume} {config_info.currency}\n
    
    Платёжная система: {config_info.payment_choices}\n
    
    Мин. % выполненых ордеров: {config_info.completed_orders_percent}%
    Мин. количество выполненых ордеров: {config_info.deals_performed}

    Мин. спред: {config_info.spread_percent}%
    
    Уведомления на активные 🟢 / паузе 🟡
    """

    reply_keyboard = [
        [text["enable_notif"], text["market_check"]],
        [text["modifying"], text["deleting"]],
        [text["return"]]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=message_text, reply_markup=markup)
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
