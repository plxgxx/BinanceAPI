""" session genation """
import pandas as pd
from functools import wraps

from data import text
from .base import Session

""" busines logic database access """
import datetime
from typing import Dict
from typing import List
from typing import Set
from typing import Tuple

from .models import Admin, User, NotificationCumfig


def local_session(function):
    """ build and close local session """

    @wraps(function)
    def wrapped(self, *args, **kwargs):
        session = Session()
        try:
            result = function(self, session, *args, **kwargs)
        except Exception as error:
            # in case commit wan't be rolled back next trasaction failed
            session.rollback()
            raise ValueError(error) from error  # notify developer

        session.close()
        return result

    return wrapped



class DBSession():
    """ db function with renewadle session for each func """

    def __init__(self):
        self.admins = []

    @local_session
    def get_admin(self, session, chat_id) -> None:
        admin = session.query(Admin).get(chat_id)
        return admin

    @local_session
    def get_admins(self, session, role_list) -> None:
        admins = (
            session.query(Admin.chat_id)
            .filter(Admin.role.in_(role_list))
            .all()
        )

        return admins

#### User.is_admin defines whether to count user in general user list
    @local_session
    def make_admin(self, session, chat_id, role) -> None:

        if role == "superadmin" or role == "sales":
            user = session.query(User).get(chat_id)
            user.is_admin = True  # not count as user
            session.commit()
        elif role == "user":
            user = session.query(User).get(chat_id)
            user.is_admin = False  # count as user
            session.commit()
        
        admin = session.query(Admin).get(chat_id)

        if admin:
            admin.role = role
            session.commit()
            return admin
        
        new_admin = Admin(
            chat_id=chat_id,
            role=role
        )
        session.add(new_admin)
        session.commit()

        return new_admin
    
    @local_session
    def remove_admin(self, session, chat_id):
        old_admin = session.query(Admin).get(chat_id)
        session.delete(old_admin)
        old_admin = session.query(User).get(chat_id)
        old_admin.is_admin = False
        session.commit()

    @local_session
    def add_user(self, session, user_data: Dict) -> User:
        """
        Create user record if not exist, otherwise update username
        """
        chat_id = user_data["chat_id"]
        username = user_data["username"]
        first_name = user_data["first_name"]
        last_name = user_data["last_name"]
        language = user_data["language"]
        time_registered = user_data["time_registered"]
        is_admin = False

        user = session.query(User).get(chat_id)
        if user:
            if user.username != username:
                user.username = username
                session.commit()
            if user.is_banned is True:
                user.is_banned = False
                session.commit()
            return user

        new_user = User(
            chat_id=chat_id,
            is_banned=False,
            username=username,
            first_name=first_name,
            last_name = last_name,
            language = language,
            time_registered = time_registered,
            is_admin = is_admin,
        )
        session.add(new_user)
        session.commit()
        return new_user

    @local_session
    def delete_user(self, session, chat_id):
        old_user = session.query(User).get(chat_id)

        session.query(Admin).filter(Admin.chat_id==old_user.chat_id).delete(synchronize_session=False)
        session.query(NotificationCumfig).filter(NotificationCumfig.user_id==old_user.chat_id).delete(synchronize_session=False)

        session.delete(old_user)
        session.commit()

    @local_session
    def ban_user(self, session, chat_id: int) -> None:
        """ user banned the bot """

        user = session.query(User).get(chat_id)
        if user and user.is_banned is False:
            user.is_banned = True
            session.commit()

    @local_session
    def unban_user(self, session, chat_id: int) -> None:
        """ user started conversation after ban """

        user = session.query(User).get(chat_id)
        if user.is_banned is True:
            user.is_banned = False
            session.commit()


    @local_session
    def get_user(self, session, chat_id) -> Tuple[int, str, str]:
        """ return universi_id and user date for engine.API call """
        user = session.query(User).get(chat_id)
        return user


    @local_session
    def get_users_name(self, session) -> Tuple[int, str, str]:
        """ return universi_id and user date for engine.API call """
        users = (
            session.query(User.chat_id, User.first_name, User.last_name)
            .filter(User.is_admin==False)
            .all()
        )
        return users

    @local_session
    def get_users_admins_name(self, session) -> Tuple[int, str, str]:
        """ return universi_id and user date for engine.API call """
        users = (
            session.query(User.chat_id, User.first_name, User.last_name)
            .all()
        )
        return users

    @local_session
    def count_users(self, session) -> int:
        """ number of users in our db """

        users_quantity = session.query(User).count()
        return users_quantity

    @local_session
    def get_users_list(self, session):
        """ list all users in database """

        users = session.query(User.chat_id).filter(User.is_admin==False).all()
        return users

    @local_session
    def get_users_list_full(self, session):
        """ list all users in database """

        users = session.query(
            User.chat_id,
            User.is_banned,
            User.username,
            User.first_name,
            User.last_name,
            User.time_registered
            ).filter(User.is_admin==False).all()
        return users

    @local_session
    def get_users_list_obj(self, session, reminder_time=None):
        """ list all users in database """
        if reminder_time == None:
            users = session.query(
                User
                ).filter(User.is_admin==False).all()
        else:
            users = session.query(
                User
                ).filter(
                    User.is_admin==False,
                    User.reminder_time==reminder_time
                ).all()

        return users

    @local_session
    def get_users_admins_list(self, session):
        """ list all users in database """

        users = session.query(User.chat_id).all()
        return users

    @local_session
    def add_config(self, session, user_data):
        chat_id = user_data["chat_id"]
        name = user_data["config_name"]
        currency = user_data["chosen_currency"]
        payment_choices = str(user_data["chosen_methods"])
        sale_volume = user_data["amount_selling"]
        buy_volume = user_data["amount_buying"]
        spread_percent = user_data["spread_amount"]
        completed_orders_percent = user_data["order_amount"]
        deals_performed = user_data["deals_amount"]
        time_added = user_data["added_at"]




        new_config = NotificationCumfig(
            user_id=chat_id,
            is_alert=False,
            name=name,
            currency=currency,
            payment_choices=payment_choices,
            sale_volume=sale_volume,
            buy_volume=buy_volume,
            spread_percent=spread_percent,
            completed_orders_percent=completed_orders_percent,
            deals_performed=deals_performed,
            added_at=time_added,
        )
        session.add(new_config)
        session.commit()
        return new_config
         
    @local_session
    def get_configs_list(self, session, user_id):
        user_configs = session.query(NotificationCumfig.name).filter_by(user_id=user_id).all()
        return user_configs

    @local_session
    def get_config_info(self, session, chat_id, name):
        config_info = session.query(NotificationCumfig).filter_by(user_id=chat_id,name=name).first()
        return config_info

    @local_session
    def delete_config(self, session, chat_id, name):
        deleting_config = session.query(NotificationCumfig).filter_by(user_id=chat_id, name=name).first()

        session.delete(deleting_config)
        session.commit()
        return deleting_config

    @local_session
    def edit_name(self, session, chat_id, arg_to_change, old_arg, new_arg):
        config_obj = session.query(NotificationCumfig).filter_by(user_id=chat_id, name=old_arg).first()
        if arg_to_change == text["name"]:
            config_obj.name = new_arg
        elif arg_to_change == text["volume_b"]:
            config_obj.buy_volume = new_arg
        elif arg_to_change == text["volume_s"]:#ERROR
            config_obj.sale_volume = new_arg
        elif arg_to_change == text["payment_c"]:
            config_obj.payment_choices = new_arg
        elif arg_to_change == text["%orders"]:
            config_obj.completed_orders_percent = new_arg
        elif arg_to_change == text["deals"]:
            config_obj.deals_performed = new_arg
        elif arg_to_change == text["%spread"]:
            config_obj.spread_percent = new_arg
        session.commit()



db_session: DBSession = DBSession()
