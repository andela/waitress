from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
import json


class SlackUserManager(models.Manager):
    """
    A class that manages `SlackUser` model
    """
    def __init__(self, *args):
        """
        A initialization method that setup methods and properties of this class
        from its parent
        """
        super(SlackUserManager, self).__init__()

    def create_user(self, *args, **kwargs):
        """
        An instance method that creates a new user
        """
        return SlackUser(**kwargs)


class SlackUser(AbstractBaseUser):
    """
    A class that represents a `SlackUser` account
    """
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
        """
        A class method that creates a new user
        """
        return cls.objects.create(**user_data_dict)

    def __unicode__(self):
        """
        An instance method that return a string representation of this model
        """
        return "{} {} {}".format(str(self.id), self.firstname, self.lastname)

    def is_tapped(self):
        time_now = timezone.now()
        date_today = time_now.date()
        mealservice = self.mealservice_set.filter(date=date_today)
        if not mealservice.count():
            return False
        if 0 < time_now.hour < 12:
            return mealservice[0].breakfast
        return mealservice[0].lunch


def untapped_default():
    """
    A method that sets the default field value
    """
    return json.dumps([])


class JSONField(models.TextField):
    """
    A custom JSON field
    """
    description = "A JSON field representing a untapped event"

    def __init__(self, value, *args, **kwargs):
        self.value = value
        super(JSONField, self).__init__(args)

    def deconstruct(self):
        """
        A method which deconstructs a JSON value for db entry
        """
        name, path, args, kwargs = super(JSONField, self).deconstruct()
        # Only include kwarg if it's not the default
        if self.value != "":
            kwargs['value'] = json.dumps(self.value)
        else:
            kwargs['value'] = json.dumps(kwargs.get('default')())
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection, context):
        """
        A method which recontructs a JSON value from its db entry
        """
        if value == '':
            return self.value
        value = value.replace("'", '"')
        return json.loads(str(value))

    def to_python(self, value):
        """
        A method which recontructs a JSON value/dict from its db entry
        """
        if value == '':
            return self.value
        return json.loads(value)


class MealService(models.Model):
    """
    A model that represents a meal service record for a day
    """
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    user = models.ForeignKey(SlackUser)
    untapped = JSONField('Untapped', default=untapped_default, blank=True)
    date = models.DateField()
    date_modified = models.DateTimeField(null=True)

    @classmethod
    def create(cls, service_dict):
        """
        A method that creates a meal served data record
        """
        return cls.objects.create(**service_dict)

    def __unicode__(self):
        """
        A method that returns a printable representation of the model
        """
        has_untapped = len(self.untapped) != 0
        return "{user} {has_breakfast} {has_lunch} {has_untapped} {date}"\
            .format(
                user=self.user_id, has_breakfast=self.breakfast,
                has_lunch=self.lunch, has_untapped=has_untapped,
                date=self.date)


class Passphrase(models.Model):
    """
    A model that represents a passphrase
    """
    word = models.CharField(max_length=100, unique=True)


class MealSession(models.Model):
    """
    A model that represents a meal session
    """
    status = models.BooleanField(default=False)
    date = models.DateField()

    @classmethod
    def in_progress(cls):
        """
        A property that returns meal session for the current day
        """
        return cls.objects.filter(date=timezone.now().date(), status=True)
