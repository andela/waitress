import random
import re
import string

import pytz
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from slacker import Slacker

from app.models import SlackUser

slack = Slacker(settings.SLACK_API_TOKEN)


class UserRepository(object):
    """
    A wrapper class for methods that update the list of users.
    """

    @staticmethod
    def manual_transaction(records):
        transaction.set_autocommit(False)
        for record in records:
            record.save()
        transaction.commit()
        transaction.set_autocommit(True)

    @staticmethod
    def regularize_guests():
        """ Regularize guest names"""
        ordered_guests = SlackUser.objects.filter(
            firstname__startswith="Guest"
        ).order_by("id")
        regularized_guests = regularize_guest_names(list(ordered_guests))
        try:
            UserRepository.manual_transaction(regularized_guests)
            return True
        except AttributeError:
            return False

    @staticmethod
    def generate_unique(user_type, ids):
        """Generates unique id for a user type.
        """
        dict_ids = {}
        uc_first_letter = user_type[0].upper()
        alphabet = string.ascii_uppercase + string.digits

        for i in ids:
            dict_ids[i] = True  # make a dictionary of ids for quick lookup.

        def gen_id():  # generate 8-char id.
            return "{0}{1}".format(
                uc_first_letter, "".join([random.choice(alphabet) for _ in range(8)])
            )

        new_id = gen_id()

        while True:
            new_id = gen_id()
            if not dict_ids.get(new_id):
                break
            else:
                continue

        return new_id  # unique_id

    @classmethod
    def add(cls, **kwargs):
        utype = kwargs.get("utype")
        users = SlackUser.objects.filter(user_type=utype).order_by("id")
        if kwargs.get("utype").lower() != "guest":
            user = SlackUser(
                firstname=kwargs.get("firstname"), lastname=kwargs.get("lastname")
            )
        else:
            last_guest = (
                filter(lambda x: x.firstname.startswith("Guest"), list(users))[-1]
                if len(users)
                else None
            )

            if not last_guest:
                username = kwargs.get("name", "Guest 1")
            else:
                last_num = int(
                    re.match("^Guest ([\d]*)".format(), last_guest.firstname).groups()[
                        0
                    ]
                )

                username = "Guest {}".format(last_num + 1)

            user = SlackUser(firstname=username)

        user.slack_id = cls.generate_unique(
            utype, [individual.slack_id for individual in users] if len(users) else []
        )
        user.user_type = utype

        try:
            user.save()
            return (
                "{} ({}) was created successfully.".format(user.firstname, utype),
                user.id,
            )

        except Exception as e:
            user_type = utype.upper()
            error_type = type(e)
            return f"{user_type} user couldn't be created. Error: {error_type}"

    @classmethod
    def update(cls, trim=False):
        """
        A method that update the user records.

        :param:
        trim:= determines if old users should be removed from the database.
        """
        group_info = slack.groups.info(settings.SLACK_GROUP)
        user_info = slack.users.list()
        if group_info.successful:
            members = group_info.body["group"]["members"]
            cls.user_queryset = SlackUser.objects.all()
            difference = cls.difference(members, cls.user_queryset)

            if len(difference):
                # get user info
                if user_info.successful:
                    return cls.filter_add_user(
                        user_info.body["members"], difference, trim
                    )
            else:
                return "Users list wasn't changed."

    @classmethod
    def difference(cls, repo_users, db_users):
        """
        A method that gets the difference between users in the system and
        users in slack group.
        """
        users = [user.slack_id for user in db_users]

        # return all users from slack that don't exist in the db
        return [user for user in repo_users if user not in users]

    @classmethod
    def is_user_invalid(cls, user):
        is_deleted = user.get("deleted")
        is_bot = user.get("is_bot")
        email = user.get("profile").get("email", "")
        is_email_valid = email.endswith(settings.DOMAIN_LIST)

        return is_deleted or is_bot or (not is_email_valid)

    @classmethod
    def _construct_user_details(cls, item):
        firstname = item.get("profile").get("first_name", "")
        lastname = item.get("profile").get("last_name", "")
        return {
            "slack_id": item["id"],
            "email": item["profile"]["email"],
            "photo": item["profile"].get(
                "image_original", item["profile"].get("image_192")
            ),
            "firstname": firstname.title(),
            "lastname": lastname.title(),
        }

    @classmethod
    def normalize(cls, info):
        """
        A function that normalizes retrieved information from Slack.
        """
        invalid_users = [item["id"] for item in info if cls.is_user_invalid(item)]
        valid_users = {
            item["id"]: cls._construct_user_details(item)
            for item in info
            if not cls.is_user_invalid(item)
        }

        return valid_users, invalid_users

    @classmethod
    def filter_add_user(cls, info, difference, trim):
        """
        A method that retrieves users' info using the difference.
        """

        valid_users, invalid_users = cls.normalize(info)

        valid_slack_users = [user for user in difference if user not in invalid_users]

        if not valid_slack_users:
            return "No new user found on slack."

        if trim:
            return cls.trim_away(invalid_users)

        try:
            for user_slack_id in valid_slack_users:
                current_user = valid_users[user_slack_id]
                with transaction.atomic():
                    SlackUser.create(current_user)
            return "Users updated successfully."
        except Exception as e:
            return f"Users couldn't be updated successfully - {e.args[0]}"

    @classmethod
    def trim_away(cls, invalid_users):
        """Trims away users for the system that have been deleted off Slack."""
        deleted_users = [
            user.delete()
            for user in cls.user_queryset
            if user.slack_id in invalid_users
        ]

        number_of_deleted_users = len(deleted_users)
        if number_of_deleted_users:
            return f"{number_of_deleted_users} Users deleted"
        return "There are no invalid users found on slack."


class Time:
    """
    A class that with methods for time time functions.
    """

    @classmethod
    def is_before_midday(cls):
        """
        A method that return True if the time is before midday.
        """
        timezone.activate(pytz.timezone("Africa/Lagos"))
        time = timezone.now().hour
        if 0 < time < 12:
            return True
        return False


def regularize_guest_names(guest_list):
    """Regularizes the names of guest.
    """
    guest_list_cp = guest_list[:]
    number_of_guests = len(guest_list_cp)
    for i in range(number_of_guests):
        guest_list_cp[i].firstname = "Guest {}".format(i + 1)
    return guest_list_cp
