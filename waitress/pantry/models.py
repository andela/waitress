from django.db import models
from app.models import SlackUser

# Create your models here.
class Pantry(models.Model):
    """
    Model representing the pantry service
    """

    id = models.AutoField(unique=True, primary_key=True)
    user = models.ForeignKey(SlackUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    @classmethod
    def is_tapped(cls, user_id):
        service = cls.objects.filter(user_id=user_id, date=date.today()).first()
        return service
