from app.models import SlackUser
from app.serializers import UserSerializer
from django.conf import settings
from slacker import Slacker
import re

slack = Slacker(settings.SLACK_API_TOKEN)


class UserRepository(object):
    """
    A wrapper class for methods that update the list of users
    """

    @classmethod
    def update(cls):
        """
        A method that update the user records
        """
        group_info = slack.groups.info(settings.SLACK_GROUP)
        user_info = slack.users.list()
        if group_info.successful:
            members = group_info.body['group']['members']
            user_queryset = SlackUser.objects.all()
            difference = cls.difference(members, user_queryset)

            if len(difference):
                # get user info
                if user_info.successful:
                    return cls.filter_add_user(
                        user_info.body['members'], difference
                    )
            else:
                return "Users list is remains unchanged"

    @classmethod
    def difference(cls, repo_users, db_users):
        """
        A method that gets the difference between users in the system and
        users in slack group
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
    def filter_add_user(cls, info, difference):
        """
        A method that retrieves users' info using the difference
        """
        def normalize(info):
            """ A function that normalizes retrieved information from Slack
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

        try:
            difference_copy = difference[:]
            for item in difference_copy:
                if item in not_user:
                    difference.remove(item)
            if len(difference) == 0:
                return "Users list not changed"
            for user in difference:
                if user in info:
                    SlackUser.create(info[user])
            return "Users updated successfully"
        except Exception:
            return "Users couldn't be updated successfully"
