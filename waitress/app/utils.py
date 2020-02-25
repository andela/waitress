import random
import re
import string

import pytz
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from slack import WebClient

from app.models import SlackUser


client = WebClient(token=settings.SLACK_API_TOKEN)


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
            # for some reason filter object is not subscriptable
            # last_guest = (
            #     filter(lambda x: x.firstname.startswith("Guest"), list(users))[-1]
            #     if len(users)
            #     else None
            # )
            guests = [x for x in list(users) if x.firstname.startswith("Guest")]
            last_guest = guests[-1] if len(guests) else None

            if not guests:
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
    def get_all_slack_users(cls):
        result = []
        status = None
        cursor = None
        initial_round = True

        while initial_round or cursor:
            initial_round = False
            kwargs = {}
            if cursor:
                kwargs["cursor"] = cursor
            users = client.users_list(**kwargs)
            result.extend(users.data["members"])
            cursor = users.data.get("response_metadata", {}).get("next_cursor")
            status = users.data["ok"]

        return result, status

    @classmethod
    def update(cls):
        """
        A method that update the user records.

        :param:
        """
        workspace_members, status = cls.get_all_slack_users()
        group_info = client.groups_info(channel=settings.SLACK_GROUP)

        if group_info.data["ok"]:
            members = group_info.data["group"]["members"]
            cls.user_queryset = SlackUser.objects.all()
            new_users = cls.difference(members, cls.user_queryset)

            if len(new_users):
                if status:
                    return cls.filter_add_user(workspace_members, new_users)
            return "Users list wasn't changed."
        return "Cant connect to slack."

    @classmethod
    def difference(cls, channel_members, queryset):
        """
        A method that gets the difference between users in the system and
        users in slack group.
        """
        db_users = [record.slack_id for record in queryset]
        return list(set(channel_members) - set(db_users))

    @classmethod
    def is_user_invalid(cls, user):
        is_deleted = user.get("deleted")
        is_bot = user.get("is_bot")
        email = user.get("profile").get("email", "")
        is_email_valid = email.endswith(settings.DOMAIN_LIST)

        return is_deleted or is_bot or (not is_email_valid)

    @classmethod
    def _construct_user_details(cls, user_info):
        firstname = user_info.get("profile").get("first_name", "")
        lastname = user_info.get("profile").get("last_name", "")
        return {
            "slack_id": user_info["id"],
            "email": user_info["profile"]["email"],
            "photo": user_info["profile"].get(
                "image_original", user_info["profile"].get("image_192")
            ),
            "firstname": firstname.title(),
            "lastname": lastname.title(),
        }

    @classmethod
    def normalize(cls, users):
        """
        A function that normalizes retrieved information from Slack.
        """
        valid_users = {}
        invalid_users = []

        for user in users:
            user_id = user.get("id")
            is_user_invalid = cls.is_user_invalid(user)
            if is_user_invalid:
                invalid_users.append(user_id)
            else:
                valid_users[user_id] = cls._construct_user_details(user)

        return valid_users, invalid_users

    @classmethod
    def filter_add_user(cls, workspace_members, new_users):
        """
        A method that retrieves users' info using the difference.
        # """

        valid_users, invalid_users = cls.normalize(workspace_members)

        users_to_be_added = [
            user
            for user in new_users
            if user not in invalid_users
        ]

        if not users_to_be_added:
            return "No new user found on slack."

        try:
            with transaction.atomic():
                cls._add_new_users(users_to_be_added, valid_users)
                cls._deactivate_invalid_users(invalid_users)
            return "Users updated successfully."
        except Exception as e:
            return f"Users couldn't be updated successfully - {e.args[0]}"

    @classmethod
    def _deactivate_invalid_users(cls, invalid_users):
        """Deactivate users for the system that have been deleted off Slack."""

        for user in cls.user_queryset:
            if user.slack_id in invalid_users:
                user.is_active = False
                user.save()

    @classmethod
    def _add_new_users(cls, users_to_be_added, valid_users):
        for user_slack_id in users_to_be_added:
            current_user = valid_users[user_slack_id]
            SlackUser.create(current_user)


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


def serialize_meal_service(queryset):
    return [
        {
            "firstname": x.user.firstname,
            "lastname": x.user.lastname,
            "email": x.user.email,
            "hadBreakfast": x.breakfast,
            "hadLunch": x.lunch,
            "userId": x.user.id,
        }
        for x in queryset
    ]
