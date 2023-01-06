from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from states import *
from telegram.ext import ConversationHandler
from data import text
from database import db_session
import datetime
from data import TIME_ZONE


def start(update, context):

    msg = update.message.text
    chat_id = update.message.chat.id

    authorized_users = db_session.get_users_admins_list()
    authorized_users = [user[0] for user in authorized_users]

    if chat_id not in authorized_users: #DB.authorized_ids 
        context.bot.send_message(chat_id = chat_id, text = text["non-authorized"],reply_markup=ReplyKeyboardRemove(),)
        return States.PASSWORD_CHECK
        
    reply_keyboard = [
        [text["binance"], "Binance P2P с конвертацией(Позже)"],
        ["Мои уведомления(Позже)", text["manage"]]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text=text["start"], reply_markup=markup)
    return States.MAIN_MENU


def password_check(update, context):

    msg = update.message.text
    chat_id = update.message.chat.id
    
    authorized_users = db_session.get_users_admins_list()
    authorized_users = [user[0] for user in authorized_users]
    if chat_id in authorized_users:
        return start(update, context)
    
    #admin_passwords = ["1212", "5070"]
    leadgen_password = "паляниця" #["4224", "1218"]  #from DB

    if msg in []:#admin_passwords:
        pass
    elif msg == leadgen_password:
        context.bot.send_message(chat_id = chat_id, text = text["enter_name"])
        return States.NAME_AND_SURNAME
    else:
        context.bot.send_message(chat_id = chat_id, text = text["wrong_password"])
        return States.PASSWORD_CHECK


def get_name_surname(update, context):

    msg = update.message.text
    chat_id = update.message.chat.id
    
    name = msg.split(" ")
    if len(name) != 2:
        context.bot.send_message(chat_id = chat_id, text = text["wrong_name_format"])
        return States.NAME_AND_SURNAME
    
    first_name = name[0]
    last_name = name[1]
    username = update.effective_chat.username
    chat_id = update.effective_chat.id
    time_registered = datetime.datetime.now(tz=TIME_ZONE)

    context.user_data["first_name"] = first_name
    context.user_data["last_name"] = last_name
    context.user_data["language"] = "ru"
    context.user_data["username"] = username
    context.user_data["chat_id"] = chat_id
    context.user_data["time_registered"] = time_registered

    db_session.add_user(context.user_data)

    context.user_data.clear()

    context.bot.send_message(chat_id = chat_id, text = text["authorized_successfully"] % (str(first_name) + " " + str(last_name)))

    return start(update, context)


def done(update, context):
    return ConversationHandler.END


def faq(update, context):
    chat_id = update.message.chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text=text["faq"]
    )
    return ConversationHandler.END


def echo_service(update, context):
    """ echo all msgs"""

    chat_id = update.message.chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text=(
            "Зараз бот на технічному обслуговуванні ⚠\n"
            + "и тимчасово не працює 🧑🏿‍💻\nСкоро повернемось🕔"
        ),
    )

