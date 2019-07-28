import time

from django.conf import settings
from slacker import Slacker


slack = Slacker(settings.SLACK_API_TOKEN)


def fetch_channel_members():
    group_info = slack.groups.info(settings.SLACK_GROUP)
    members = group_info.body["group"]["members"]
    return members


def get_all_slack_users():
    return slack.users.list()


def get_new_members(all_users):
    pass


def generate_guest_id():
    return f"G{time.time()}"


def manual_user_serializer(queryset):
    result = []
    for user in queryset:
        user_data = dict(
            firstname=user.firstname,
            email=user.email,
            slack_id=user.slack_id,
            id=user.id,
            lastname=user.lastname,
            is_active=user.is_active,
            photo=user.photo,
        )
        result.append(user_data)
    return result
