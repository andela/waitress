import logging

from django.conf import settings
from django.db import transaction
from slacker import Slacker

from waitress.app.models import SlackUser


slack = Slacker(settings.SLACK_API_TOKEN)

group_info = slack.groups.info(settings.SLACK_GROUP)
user_info = slack.users.list()

# Get an instance of a logger
logger = logging.getLogger(__name__)


def _manual_transaction(records):
    transaction.set_autocommit(False)
    for record in records:
        record.save()
    transaction.commit()
    transaction.set_autocommit(True)
    return 'Update completed!'


def _fetch_slack_users():
    user_info = slack.users.list()
    members = user_info.body.get("members", [])
    return members


def _get_user_on_slack(slack_id, slack_members):
    for member in slack_members:
        if member["id"] == slack_id:
            return member
    return None


def normalize_users():
    try:
        db_users = SlackUser.objects.filter(user_type__in=["employee", "staff"]).all()
        slack_members = _fetch_slack_users()
        null_names = []

        for user in db_users:
            if not (user.firstname and user.lastname):
                current_user = _get_user_on_slack(user.slack_id, slack_members)
                user.firstname = current_user.get("profile").get("first_name", "")
                user.lastname = current_user.get("profile").get("last_name", "")
                null_names.append(user)
                print(f"Done updating user field for {user.firstname} {user.lastname}")

        return _manual_transaction(null_names)
    except Exception as e:
        logger.error(e.args)
