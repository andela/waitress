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
