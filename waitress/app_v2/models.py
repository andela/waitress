import pytz

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone

from app_v2.constants import STAFF
from app_v2.enums import USER_ENUM
from app_v2.utils import is_before_midday


class SlackUser(AbstractBaseUser):
    """
    A class that represents a `SlackUser` account
    """

    slack_id = models.CharField(unique=True, max_length=20)
    firstname = models.CharField(max_length=50, default="")
    lastname = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=100, blank=True)
    user_type = models.CharField(max_length=30, choices=USER_ENUM, default=STAFF)
    photo = models.CharField(max_length=512, default="https://placehold.it/128x128")
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def string_repr(self):
        """
        An instance method that return a string representation of this model
        """
        return f"{self.slack_id}: {self.firstname}"

    def __repr__(self):
        return self.string_repr()

    def __str__(self):
        return self.string_repr()

    def __unicode__(self):
        return self.string_repr()

    def is_tapped(self):
        timezone.activate(pytz.timezone("Africa/Lagos"))
        date_today = timezone.now().date()
        before_midday = is_before_midday()
        meal_service = MealService.objects.filter(user=self, date=date_today).first()

        if not meal_service:
            return False

        return meal_service.breakfast if before_midday else meal_service.lunch


class MealService(models.Model):
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    user = models.ForeignKey(SlackUser, on_delete=models.CASCADE)
    date = models.DateField()

    def set_meal(self, **kwargs):
        self.breakfast = kwargs.get("breakfast")
        self.lunch = kwargs.get("lunch")
        self.save()


class MealSession(models.Model):
    status = models.BooleanField(default=False)
    date = models.DateField()

    @classmethod
    def get_meal_session(cls):
        """
        A property that returns meal session for the current day
        """
        timezone.activate(pytz.timezone("Africa/Lagos"))
        date_today = timezone.now().date()
        return cls.objects.filter(date=date_today, status=True).first()
