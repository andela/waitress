from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.
class SlackUser(AbstractBaseUser):
    """
    A class that represents a `SlackUser` account
    """

    # Enum fields for user type.
    CHEF = "chef"
    CLEANER = "cleaner"
    GUEST = "guest"
    SECURITY = "security"
    STAFF = "staff"

    USER_TYPE = (
        (CHEF, "chef"),
        (CLEANER, "cleaner"),
        (GUEST, "guest"),
        (SECURITY, "security"),
        (STAFF, "staff"),
    )
    id = models.AutoField(unique=True, primary_key=True)
    slack_id = models.CharField(unique=True, max_length=20, blank=True)
    firstname = models.CharField(max_length=50, default="")
    lastname = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=100, blank=True)
    user_type = models.CharField(max_length=30, choices=USER_TYPE, default=STAFF)
    objects = SlackUserManager()
    photo = models.CharField(max_length=512, default="")
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = "id"

    @classmethod
    def create(cls, user_data_dict):
        """
        A class method that creates a new user
        """
        return cls.objects.create(**user_data_dict)

    def string_repr(self):
        """
        An instance method that return a string representation of this model
        """
        return f"{self.id}: {self.firstname} - {self.slack_id}"
