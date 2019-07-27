from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from app_v2.constants import STAFF
from app_v2.enums import USER_ENUM


class SlackUser(models.Model):
    """
    A class that represents a `SlackUser` account
    """

    slack_id = models.CharField(
        unique=True, max_length=20, blank=True, primary_key=True
    )
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


class MealSession(models.Model):
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    user = models.ForeignKey(SlackUser, on_delete=models.CASCADE)
    date = models.DateField()
