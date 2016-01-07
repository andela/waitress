import json
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone


class SlackUserManager(models.Manager):
    '''Manages `SlackUser` model'''
    def __init__(self, *args):
        super(SlackUserManager, self).__init__()

    def create_user(self, *args, **kwargs):
        '''Create a new user'''
        return SlackUser(**kwargs)


class SlackUser(AbstractBaseUser):
    '''Represents a `SlackUser` account'''
    id = models.IntegerField(unique=True, primary_key=True)
    slack_id = models.CharField(unique=True, max_length=20)
    firstname = models.CharField(max_length=20,)
    lastname = models.CharField(max_length=20,)
    email = models.CharField(max_length=60,)
    objects = SlackUserManager()
    photo = models.CharField(max_length=512, default="",)
    USERNAME_FIELD = 'id'

    @classmethod
    def create(cls, user_data_dict):
        '''Creates a new user'''
        # import pdb; pdb.set_trace()
        return cls.objects.create(**user_data_dict)

    def __unicode__(self):
        return "{} {} {}".format(str(self.id), self.firstname, self.lastname)


def untapped_default():
    return json.dumps([])


class JSONField(models.TextField):
    description = "A JSON field representing a untapped event"

    def __init__(self, value, *args, **kwargs):
        self.value = value
        super(JSONField, self).__init__(args)

    def deconstruct(self):
        name, path, args, kwargs = super(JSONField, self).deconstruct()
        # Only include kwarg if it's not the default
        if self.value != "":
            kwargs['value'] = json.dumps(self.value)
        else:
            kwargs['value'] = json.dumps(kwargs.get('default')())
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection, context):
        if value == '':
            return self.value
        value = value.replace("'", '"')
        return json.loads(str(value))

    def to_python(self, value):
        if value == '':
            return self.value
        return json.loads(value)


class Service(models.Model):
    '''Represents a service record for a day'''
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    user = models.ForeignKey(SlackUser)
    untapped = JSONField('Untapped', default=untapped_default, blank=True)
    date = models.DateField()
    date_modified = models.DateTimeField(null=True)

    @classmethod
    def create(cls, service_dict):
        '''Creates a served data record'''
        return cls.objects.create(**service_dict)

    def __unicode__(self):
        has_untapped = len(self.untapped) != 0
        return "{user} {has_breakfast} {has_lunch} {has_untapped} {date}"\
            .format(
                user=self.user_id, has_breakfast=self.breakfast,
                has_lunch=self.lunch, has_untapped=has_untapped,
                date=self.date)


class Passphrase(models.Model):
    '''Represents a passphrase'''
    word = models.CharField(max_length=100, unique=True)


class MealSession(models.Model):
    '''Represents a meal session'''
    status = models.BooleanField(default=False)
    date = models.DateField()

    @property
    def in_progress(self):
        return MealSession.objects.get(date=timezone.now().date())
