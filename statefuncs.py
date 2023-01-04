from telegram import ReplyKeyboardMarkup
from states import *
from telegram.ext import ConversationHandler
from data import text


def start(update, context):
    reply_keyboard = [
        [text["binance"], "Binance P2P с конвертацией(Позже)"],
        ["Мои уведомления(Позже)", text["manage"]],
        [text["done"]]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["start"], reply_markup=markup)
    return States.MAIN_MENU


def done(update, context):
    return ConversationHandler.END


def faq(update, context):
    chat_id = update.message.chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text=text["faq"]
    )
    return ConversationHandler.END


