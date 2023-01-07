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
    chat_id = update.message.chat.id
    msg = update.message.text
    context.user_data["config_name"] = msg
    config_info = db_session.get_config_info(chat_id, msg)
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
        [text["name"], text["volume_b"], text["volume_s"]],
        [text["payment_c"], text["min_orders_perc"], text["min_deals_amount"], text["min_spread_perc"]],
        [text["manage"], text["return"]]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["modify"], reply_markup=markup)
    return States.SETTING_MODIFY


def delete_config(update, context):
    chat_id = update.message.chat.id
    reply_keyboard = [
        [text["yes"], text["no"]]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["delete"], reply_markup=markup)
    db_session.delete_config(chat_id, context.user_data["config_name"])
    return States.SETTING_DELETE


def succesfull_delete(update, context):
    update.message.reply_text(text=text["deleted"])
    return start(update, context)


def modify_name (update, context):
    msg = update.message.text
    if msg == text["name"]:
        update.message.reply_text(text="Введите новое название конфигурации")
        context.chat_data["arg_to_change"] = text["name"]
    elif msg == text["volume_b"]:
        update.message.reply_text (text="Введите новый объём продаж")
        context.chat_data["arg_to_change"] = text["volume_s"]
    elif msg == text["volume_s"]:
        update.message.reply_text(text="Введите новый объём покупки")
        context.chat_data["arg_to_change"] = text["volume_b"]
    elif msg == text["payment_c"]:
        reply_keyboard = [
            ["Revolut","Wise","SkrillMoneyBookers"],
            ["Adcash","ZEN"],
            [text["return"]]
        ]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text (text="Введите новый способ оплаты", reply_markup=markup)
        context.chat_data["arg_to_change"] = text["payment_c"]
    elif msg == text["min_orders_perc"]:
        update.message.reply_text(text="Введите мин. % выполненых ордеров")
        context.chat_data["arg_to_change"] = text["min_orders_perc"]
    elif msg == text["min_deals_amount"]:
        update.message.reply_text(text="Введите мин количество выполненых ордеров")
        context.chat_data["arg_to_change"] = text["min_deals_amount"]
    elif msg == text["min_spread_perc"]:
        update.message.reply_text (text="Введите новый мин. % спреда")
        context.chat_data["arg_to_change"] = text["min_spread_perc"]

    return States.MODIFY_NAME


def modify_name_complete(update, context):
    chat_id = update.message.chat.id
    msg = update.message.text
    db_session.edit_name(chat_id=chat_id, arg_to_change=context.chat_data["arg_to_change"], old_arg=context.user_data["config_name"], new_arg=msg)
    return config_choice(update, context)


