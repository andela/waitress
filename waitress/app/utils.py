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
                users.setdefault(user.get('slack_id'), 0)

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
                if not getattr(item, 'deleted', False) and not getattr(
                        item, 'is_bot', False):
                    if 'image_original' not in item['profile']:
                        continue
                    if 'email' not in item['profile']:
                        continue
                    print item['profile']['email']
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
            return user_dict

        info = normalize(info)

        try:
            not_person = []
            for user in difference:
                if user in info:
                    SlackUser.create(info[user])
                else:
                    not_person.append(user)
            if len(not_person):
                return "Users list not changed"
            return "Users updated successfully"
        except Exception:
            return "Users couldn't be updated successfully"
