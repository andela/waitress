from app.models import SlackUser
from django.conf import settings
import pytz
import re
import string
import random
from django.utils import timezone
from django.db import transaction
from slacker import Slacker


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
            firstname__startswith='Guest').order_by('id')
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
        alphabet = string.uppercase + string.digits

        for i in ids:
            dict_ids[i] = True  # make a dictionary of ids for quick lookup.

        def gen_id():  # generate 8-char id.
            return "{0}{1}".format(
                uc_first_letter,
                ''.join([random.choice(alphabet) for _ in range(8)]))

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
        utype = kwargs.get('utype')
        users = SlackUser.objects.filter(user_type=utype).order_by('id')
        if kwargs.get("utype") != "guest":
            user = SlackUser(
                firstname=kwargs.get("firstname"),
                lastname=kwargs.get("lastname"),)
        else:
            last_guest = filter(lambda x: x.firstname.startswith("Guest"),
                                list(users))[-1] if len(users) else None

            if not last_guest:
                username = kwargs.get("name", "Guest 1")
            else:
                last_num = int(
                    re.match("^Guest ([\d]*)".format(), last_guest.firstname).groups()[0])

                username = 'Guest {}'.format(last_num + 1)

            user = SlackUser(firstname=username)

        user.slack_id = cls.generate_unique(
            utype, [individual.slack_id for individual in users] if len(users) else [])
        user.user_type = utype

        try:
            user.save()
            return "{} ({}) was created successfully.".format(user.firstname, utype,), user.id

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

        # if user is in slack group and not in database
        for user in db_users:
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
                if 'email' not in item['profile'] or item['profile'].get('email') is None:
                    not_user_list.append(item['id'])
                    continue

                if not item['profile']['email'].endswith(settings.DOMAIN_LIST):
                    not_user_list.append(item['id'])
                    continue

                firstname = item.get('profile').get('first_name', '')
                lastname = item.get('profile').get('last_name', '')
                user_dict[item['id']] = {
                    'slack_id': item['id'],
                    'email': item['profile']['email'],
                    # use slack default image
                    'photo': item['profile'].get('image_original', item['profile'].get('image_192')),
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


def regularize_guest_names(guest_list):
    """Regularizes the names of guest.
    """
    guest_list_cp = guest_list[:]
    for i in xrange(len(guest_list_cp)):
        guest_list_cp[i].firstname = "Guest {}".format(i + 1)
    return guest_list_cp
