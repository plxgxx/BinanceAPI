from telegram import ReplyKeyboardMarkup
from states import *
from data import text


def starting_setting(update, context):
    reply_keyboard = [
        ["Включить уведомления", "Проверить сейчас"],
        ["Редактировать", "Удалить"],
        ["Вернуться в главное меню"]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["starting"], reply_markup=markup)
    return States.SETTING_WELCOME


def notification_text(update, context):
    reply_keyboard = [
        ["Настроить конфигурацию", "Вернуться в главное меню"]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["notification"], reply_markup=markup)
    return States.SETTING_NOTIFICATIONS


def checking_market(update, context):
    reply_keyboard = [
        ["Включить уведомления", "Проверить ещё раз"],
        ["В настройки конфигурации", "Вернуться в главное меню"]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["checking"], reply_markup=markup)
    return States.SETTING_CHECK


def setting_modify(update, context):
    reply_keyboard = [
        ["В настройки конфигурации", "Вернуться в главное меню"]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["modify"], reply_markup=markup)
    return States.SETTING_MODIFY


def delete_config(update, context):
    reply_keyboard = [
        ["Да", "Нет"]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["delete"], reply_markup=markup)
    return States.SETTING_DELETE


def succesfull_delete(update, context):
    update.message.reply_text(text=text["deleted"])
    return States.MAIN_MENU
