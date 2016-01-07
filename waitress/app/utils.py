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
            serializer = UserSerializer(user_queryset, many=True)
            difference = cls.difference(members, serializer.data)

            if len(difference):
                # get user info
                if user_info.successful:
                    cls.filter_add_user(user_info.body['members'], difference)

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
                users.setdefault(user, 0)

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
            for item in info:
                if (not getattr(item, 'deleted', False) or not getattr(
                        item, 'is_bot')):
                    if 'image_original' not in item['profile']:
                        continue
                    if 'email' not in item['profile']:
                        continue
                    firstname, lastname = re.match(
                        '^(\w+).(\w+)', item['profile']['email']).groups()
                    user_dict[item['id']] = {
                        'id': item['id'],
                        'email': item['profile']['email'],
                        'photo': item['profile']['image_original'],
                        'firstname': firstname.title(),
                        'lastname': lastname.title()
                    }
            return user_dict

        info = normalize(info)

        for user in difference:
            if user in info:
                SlackUser.create(info[user])
