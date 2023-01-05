import datetime

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from states import *
from data import text, TIME_ZONE
from database import db_session


def offer_curr_choice(update, context):
    reply_keyboard = [
        ["CHF", "SEK", "PLN"],
        ["CZK", "USD", "EUR"],
        ["UAH", "CAD", "GBP"], 
        [text["return"]]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["offer_curr_choice"], reply_markup=markup)
    return States.CURR_GIVING


def offer_payment_choice(update, context):
    # msg = update.message.text
    # chat_id = update.message.chat.id

    print(update.callback_query)

    if update.callback_query == None:
        msg = update.message.text
        context.user_data["chosen_currency"] = msg

        inline_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Revolut", callback_data="revolut"),
            InlineKeyboardButton("Wise", callback_data="wise"),
            InlineKeyboardButton("SkrillMoneyBookers", callback_data="skrillmoneybookers")],
            [InlineKeyboardButton("Adcash", callback_data="adcash"),
            InlineKeyboardButton("ZEN", callback_data="zen")],
            [InlineKeyboardButton(text["done"], callback_data="done")]
        ], resize_keyboard=True, one_time_keyboard=True)
        # update.message.edit_reply_markup(reply_markup=ReplyKeyboardRemove())
        update.message.reply_text(text=text["offer_payment_choice"], reply_markup=inline_markup)
        context.user_data["chosen_methods"] = []
    elif update.callback_query.data == "done":
        print(context.user_data["chosen_methods"])
        return offer_amount_selling(update, context)
    else:
        context.user_data["chosen_methods"].append(str(update.callback_query.data))
        print(context.user_data["chosen_methods"])
        payments_list = ["Revolut", "Wise", "SkrillMoneyBookers", "Adcash", "ZEN"]
        payments_list = [i for i in payments_list if i.lower() not in context.user_data["chosen_methods"]]
        print(payments_list)
        inline_payment_list = list(InlineKeyboardButton(i, callback_data=i.lower()) for i in payments_list)

        chat_id = update.callback_query.message.chat.id
        message_id = update.callback_query.message.message_id
        inline_markup = InlineKeyboardMarkup([
            inline_payment_list,
            [InlineKeyboardButton(text["done"], callback_data="done")]
        ], resize_keyboard=True, one_time_keyboard=True)
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text["offer_payment_choice"] + f". Выбранные методы: {context.user_data['chosen_methods']}")
        context.bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=inline_markup)


    return States.PAYMENT_TYPE


def offer_amount_selling(update, context):#ТУТ ЧИНИТЬ
    #reply_keyboard = update.text
    # update.message.reply_text(text=text["offer_amount_selling"])
    context.bot.send_message(chat_id=update.callback_query.message.chat.id, text=text["offer_amount_selling"], reply_markup=ReplyKeyboardRemove())
    return States.AMOUNT_SELLING


def offer_ammount_buying(update, context):
    msg = update.message.text
    update.message.reply_text(text=text["offer_ammount_buying"])
    context.user_data["amount_selling"] = int(msg)
    return States.AMOUNT_BUYING


def offer_spread_amount(update, context):
    msg = update.message.text
    context.user_data["amount_buying"] = int(msg)

    update.message.reply_text(text=text["offer_spread_amount"])
    return States.SPREAD_AMOUNT


def offer_order_amount(update, context):
    msg = update.message.text
    context.user_data["spread_amount"] = float(msg)
    update.message.reply_text(text=text["offer_order_amount"])
    return States.ORDER_AMOUNT


def offer_deals_amount(update, context):
    msg = update.message.text
    context.user_data["order_amount"] = float(msg)
    update.message.reply_text(text=text["offer_deals_amount"])
    return States.DEALS_AMOUNT


def order_config_naming(update, context):
    msg = update.message.text
    context.user_data["deals_amount"] = int(msg)
    update.message.reply_text(text=text["order_config_naming"])
    return States.CONFIG_NAME

def completion_message(update, context):
    time_added = datetime.datetime.now(tz=TIME_ZONE)
    context.user_data["added_at"] = time_added
    chat_id = update.message.chat.id
    context.user_data["chat_id"] = chat_id
    msg = update.message.text
    context.user_data["config_name"] = msg

    reply_keyboard = [
        [text["manage"], text["return"]]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["completion_message"], reply_markup=markup)
    print(context.user_data)
    db_session.add_config(context.user_data)
    return States.COMPLETE_CREATION
