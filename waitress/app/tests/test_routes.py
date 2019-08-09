from unittest.mock import patch

from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone
from rest_framework.test import APIRequestFactory

from app.models import Passphrase, SlackUser
from app.utils import UserRepository, regularize_guest_names
from app.viewsets import UserViewSet


def skipUnless(fn, *args, **kwargs):
    engine = settings.DATABASES["default"]["ENGINE"]
    if engine is "django.db.backends.postgresql_psycopg2":
        return fn(*args, **kwargs)


class ServiceTestCase(TestCase):
    """
    Tests service functionality.
    """

    @classmethod
    def setUpClass(cls):
        cls.data = {"passphrase": "passphrase", "before_midday": True}
        cls.passphrase = {"passphrase": "passphrase"}
        slack_user = SlackUser.objects.create(
            slack_id="U24A2R2",
            firstname="Test",
            lastname="User",
            email="testuser@mail.com",
            photo="http://...",
        )
        user = User.objects.create_user("username", password="userpassword")
        user.is_superuser = False
        user.is_staff = False
        user.save()
        cls.user_id = slack_user.id
        Passphrase.objects.create(word="passphrase")
        cls.client = Client()

        super(ServiceTestCase, cls).setUpClass()

    def test_can_view_start_session_page(self):
        """
        Tests that priviledged user can start a session.
        """
        response = self.client.get("/meal-sessions/")
        assert response.status_code is 200

    def test_can_view_finish_session_page(self):
        """
        Tests that priviledged user can finish a session.
        """
        response = self.client.post("/meal-sessions/start/", self.data)

        response = self.client.post("/meal-sessions/stop/", self.data)

        assert response.status_code is 200

    def test_can_view_alphabet_page(self):
        """
        Tests that user can view alphabets to choose from in a session.
        """
        response = self.client.post("/meal-sessions/start/", self.data)

        response = self.client.get("/users/?filter=A")

        assert response.status_code is 200

    def test_can_view_user_page(self):
        """
        Tests that user can view list of users.
        """
        response = self.client.get("/users/")

        assert response.status_code is 200

    def test_can_view_user_info(self):
        """
        Tests that priviledged user can retrieve user info securedly.
        """
        response = self.client.post("/users/1/retrieve-secure/", self.passphrase)
        assert response.status_code is 200
        self.assertIn("slack_id", str(response.content))

    def test_can_tap_breakfast(self):
        """
        Tests that user can NFC tap for breakfast.
        """
        self.data["before_midday"] = True
        self.data["slackUserId"] = "U24A2R2"
        response = self.client.post("/meal-sessions/start/", self.data)
        response = self.client.post("/users/nfctap/", self.data)
        assert response.status_code is 200

    def test_can_tap_lunch(self):
        """
        Tests that user can NFC tap for lunch.
        """
        self.data["before_midday"] = False
        self.data["slackUserId"] = "U24A2R2"
        response = self.client.post("/meal-sessions/start/", self.data)
        response = self.client.post("/users/nfctap/", self.data)
        assert response.status_code is 200

    def test_can_untap_breakfast(self):
        """
        Tests that privileged user can untap for breakfast.
        """
        self.data["before_midday"] = True
        self.data["slackUserId"] = "U24A2R2"
        response = self.client.post("/meal-sessions/start/", self.data)
        response = self.client.post("/users/nfctap/", self.data)
        response = self.client.post(
            "/users/{}/untap/".format(self.user_id), self.passphrase
        )
        assert response.status_code is 200

    def test_can_untap_lunch(self):
        """
        Tests that privileged user can untap for lunch.
        """
        self.data["before_midday"] = False
        self.data["slackUserId"] = "U24A2R2"
        response = self.client.post("/meal-sessions/start/", self.data)
        response = self.client.post("/users/nfctap/", self.data)
        response = self.client.post(
            "/users/{}/untap/".format(self.user_id), self.passphrase
        )
        assert response.status_code is 200

    @patch("app.utils.UserRepository.update", return_value=[])
    def test_can_trim_users(self, mock_user_repository_update):
        """
        Tests that old friends on Slack can be removed.
        """
        factory = APIRequestFactory()
        request = factory.get("/users/remove-old-friends/")
        UserViewSet.as_view({"get": "trim_users"})(request)
        assert mock_user_repository_update.called
        assert mock_user_repository_update.called_once_with(trim=True)

    def test_can_add_guest_user(self):
        """
        Test that guest can be added.
        """
        self.data = {"name": "Guest 1", "utype": "guest", "passphrase": "passphrase"}
        response = self.client.post("/users/add/", self.data)
        assert response.status_code is 200
        assert response.data.get("user_id")

    def test_can_add_security_officer(self):
        """
        Test that security officer can be added.
        """
        self.data = {
            "firstname": "John",
            "lastname": "Smith",
            "utype": "security",
            "passphrase": "passphrase",
        }
        response = self.client.post("/users/add/", self.data)
        assert response.status_code is 200
        assert response.data.get("user_id")

    def test_can_add_cleaning_personnel(self):
        """
        Test that cleaning personnel can be added.
        """
        self.data = {
            "firstname": "John",
            "lastname": "Smith",
            "utype": "cleaner",
            "passphrase": "passphrase",
        }
        response = self.client.post("/users/add/", self.data)
        assert response.status_code is 200
        assert response.data.get("user_id")

    @skipUnless
    def test_can_view_reports(self):
        """
        Tests that user can view reports.
        """
        time_today = timezone.now()
        date = time_today.date()
        # Do tap.
        self.data["before_midday"] = True
        response = self.client.post("/meal-sessions/start/", self.data)
        identities = ["U24A2R1", "U24A2R2", "U24A2R3", "U24A2R4"]
        for identity in identities:
            self.data["slackUserId"] = identity
            response = self.client.post("/users/nfctap/", self.data)
        # Cram reports.
        response = self.client.get("/reports/")
        assert response.status_code is 200
        self.assertIn("breakfast", response.content)
        self.assertIn("lunch", response.content)
        self.assertIn(str(date), response.content)
        # Cram reports for a period.
        year_month = time_today.strftime("%Y-%m")
        response = self.client.get("/reports/?from={0}".format(year_month))
        assert response.status_code is 200
        self.assertIn(year_month, response.content)

    def test_can_regularize_guest_names(self):
        guest_list = []
        for i in range(10):
            guest_list.append(
                type("Guest", (object,), dict(id=i, firstname="Guest {}".format(i + 2)))
            )
        regularized = regularize_guest_names(guest_list)
        assert regularized[-1].firstname == "Guest 10"

    def test_user_can_view_admin_login_page(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, "login.html")

    def test_user_redirects_to_login_page_on_login_failure(self):
        user_data = dict(username="user", password="password")
        response = self.client.post("", data=user_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, "login.html")

    def test_user_redirects_to_dashboard_page_on_login_success(self):
        user_data = dict(username="username", password="userpassword")
        response = self.client.post("", data=user_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, "dashboard.html")

    @classmethod
    def tearDownClass(cls):
        super(ServiceTestCase, cls).tearDownClass()
