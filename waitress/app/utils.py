from app.models import SlackUser
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from slacker import Slacker
import pytz
import re

slack = Slacker(settings.SLACK_API_TOKEN)


class UserRepository(object):
    """
    A wrapper class for methods that update the list of users.
    """

    @staticmethod
    def add(user_type, username):
        guests = SlackUser.objects.filter(user_type=user_type).order_by('id')
        last_guest = list(guests)[-1] if len(guests) else None
        if not last_guest:
            username = "Guest 1"
        else:
            last_num = last_guest.firstname[-1]
            username = last_guest.firstname.replace(
                            last_num,
                            str(int(last_num) + 1))
        new_guest = SlackUser()
        new_guest.firstname = username
        new_guest.user_type = user_type
        try:
            new_guest.save()
            return "Guest user was created successfully.", new_guest.id
        except Exception, e:
            return "Guest user couldn't be created. Error: %" % (type(e)), None

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
            members = group_info.body['group']['members']
            cls.user_queryset = SlackUser.objects.all()
            difference = cls.difference(members, cls.user_queryset)

            if len(difference):
                # get user info
                if user_info.successful:
                    return cls.filter_add_user(
                        user_info.body['members'], difference, trim
                    )
            else:
                return "Users list wasn't changed."

    @classmethod
    def difference(cls, repo_users, db_users):
        """
        A method that gets the difference between users in the system and
        users in slack group.
        """
        users = {}
        unsaved_users = []
        if len(db_users):
            for user in db_users:
                users.setdefault(user.slack_id, 0)

        for user in repo_users:
            if user not in users:
                unsaved_users.append(user)

        return unsaved_users

    @classmethod
    def filter_add_user(cls, info, difference, trim):
        """
        A method that retrieves users' info using the difference.
        """
        def normalize(info):
            """
            A function that normalizes retrieved information from Slack.
            """
            user_dict = {}
            not_user_list = []
            for item in info:
                if 'deleted' in item and item['deleted'] is True:
                    not_user_list.append(item['id'])
                    continue
                if 'is_bot' in item and item['is_bot'] is True:
                    not_user_list.append(item['id'])
                    continue
                if 'image_original' not in item['profile']:
                    not_user_list.append(item['id'])
                    continue
                if 'email' not in item['profile']:
                    not_user_list.append(item['id'])
                    continue

                firstname, lastname = re.match(
                    '^([\w-]+)[.]{0,1}([\w-]+){0,1}@',
                    item['profile']['email']).groups()
                lastname = '' if lastname is None else lastname
                user_dict[item['id']] = {
                    'slack_id': item['id'],
                    'email': item['profile']['email'],
                    'photo': item['profile']['image_original'],
                    'firstname': firstname.title(),
                    'lastname': lastname.title()
                }

            return user_dict, not_user_list

        info, not_user = normalize(info)

        difference = cls.get_real_users(difference[:], not_user)

        if len(difference) == 0:
            return "Users list not changed"

        if trim:
            return cls.trim_away(not_user)

        try:
            for user in difference:
                if user in info:
                    with transaction.atomic():
                        SlackUser.create(info[user])
            return "Users updated successfully"
        except Exception as e:
            return "Users couldn't be updated successfully - %s" % e.message

    @staticmethod
    def get_real_users(difference, not_user):
        """Get the users that are legit."""
        return [item for item in difference if item not in not_user]

    @classmethod
    def trim_away(cls, not_user):
        """Trims away users for the system that have been deleted off Slack."""
        trim_user = []
        for user in cls.user_queryset:
            if user.slack_id in not_user:
                trim_user.append("%s %s" % (user.firstname, user.lastname))
                user.delete()
        if len(trim_user):
            return "Users deleted: %s" % (', '.join(trim_user))
        return "Users list not changed"


class Time:
    """
    A class that with methods for time time functions.
    """

    @classmethod
    def is_before_midday(cls):
        """
        A method that return True if the time is before midday.
        """
        timezone.activate(pytz.timezone('Africa/Lagos'))
        time = timezone.now().hour
        if 0 < time < 12:
            return True
        return False
