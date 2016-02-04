from unittest import TestCase
from app.models import Passphrase, SlackUser, MealSession, MealService
from django.utils import timezone


def create_user():
    """
    Creates a user.

    :Returns: SlackUser object
    """
    user_dummy_data = {
        'slack_id': 'UX03131',
        'firstname': 'Test',
        'lastname': 'User',
        'email': 'testuser@tran.tum',
        'photo': 'inexistent_photo.jpg'
    }
    return SlackUser.create(user_dummy_data)

user = create_user()


class PassphraseModelTestCase(TestCase):
    """
    A testcase for the Passphrase model.
    """
    def test_can_crud_passphrase(self):
        # Creating passphrase.
        passphrase = Passphrase(word='very_secret', user=user)
        passphrase.save()
        self.assertIsNotNone(passphrase.id)
        # Reading passphrase.
        all_passphrase = Passphrase.objects.all()
        self.assertIn(passphrase, all_passphrase)
        # Updating passphrase.
        passphrase.word = 'changed_from_very_secret'
        passphrase.save()
        # Deleting passphrase.
        passphrase.delete()
        with self.assertRaises(Passphrase.DoesNotExist):
            Passphrase.objects.get(word='changed_from_very_secret')


class SlackUserModelTestCase(TestCase):
    """
    A testcase for the SlackUser model.
    """
    def test_can_crud_slackuser(self):
        # Reading slack user.
        all_slack_user = SlackUser.objects.all()
        self.assertIn(user, all_slack_user)
        # Updating slack user.
        user.lastname = 'Admin'
        user.save()
        self.assertIsInstance(
            SlackUser.objects.get(lastname='Admin'), SlackUser)
        # Deleting slack user.
        user.delete()
        with self.assertRaises(SlackUser.DoesNotExist):
            SlackUser.objects.get(email='testuser@tran.tum')


class MealSessionModel(TestCase):
    """
    A testcase for the MealSession model.
    """
    def test_can_crud_mealsession(self):
        # Creating meal session.
        user.save()
        date_today = timezone.now()
        mealsession = MealSession.objects.create(
            status=True, date=date_today
        )
        self.assertIsNotNone(mealsession.id)
        # Reading meal session.
        all_mealsessions = MealSession.objects.all()
        self.assertIn(mealsession, all_mealsessions)
        # Updating meal session.
        mealsession.status = False
        mealsession.save()
        self.assertIsInstance(
            MealSession.objects.get(date=date_today), MealSession)
        # Deleting meal session.
        mealsession.delete()
        with self.assertRaises(MealSession.DoesNotExist):
            MealSession.objects.get(date=date_today)


class MealServiceModel(TestCase):
    """
    A testcase for the MealService model.
    """
    def test_can_crud_mealservice(self):
        # Creating meal service.
        user.save()
        date_today = timezone.now()
        mealservice = MealService.objects.create(
            breakfast=1, lunch=0, user=user, date=date_today
        )
        self.assertIsNotNone(mealservice.id)
        # Reading meal service.
        all_mealservice = MealService.objects.all()
        self.assertIn(mealservice, all_mealservice)
        # Updating meal service.
        mealservice.lunch = 1
        mealservice.save()
        self.assertIsInstance(MealService.objects.get(
            breakfast=1, lunch=1, user=user), MealService)
        # Deleting meal service.
        mealservice.delete()
        self.assertRaises
        with self.assertRaises(MealService.DoesNotExist):
            MealService.objects.get(user=user)
