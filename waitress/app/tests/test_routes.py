from django.test import TestCase, Client
from app.models import Passphrase, SlackUser
from django.utils import timezone
from django.conf import settings


def skipUnless(fn, *args, **kwargs):
    engine = settings.DATABASES['default']['ENGINE']
    if engine is 'django.db.backends.postgresql_psycopg2':
        return fn(*args, **kwargs)


class ServiceTestCase(TestCase):
    """
    Tests service functionality.
    """
    @classmethod
    def setUpClass(cls):
        cls.data = {
            "passphrase": "passphrase",
            "before_midday": True,
        }
        cls.passphrase = {
            'passphrase': 'passphrase'
        }
        SlackUser.objects.create(
            slack_id="U24A2R2", firstname="Test", lastname="User",
            email="testuser@mail.com", photo="http://...",
        )
        Passphrase.objects.create(word='passphrase', user_id=1)
        cls.client = Client()

        super(ServiceTestCase, cls).setUpClass()

    def test_can_view_start_session_page(self):
        """
        Tests that priviledged user can start a session.
        """
        response = self.client.get("/meal-sessions/",)
        self.assertEquals(response.status_code, 200)

    def test_can_view_finish_session_page(self):
        """
        Tests that priviledged user can finish a session.
        """
        response = self.client.post("/meal-sessions/start/", self.data)

        response = self.client.post("/meal-sessions/stop/", self.data)

        self.assertEquals(response.status_code, 200)

    def test_can_view_alphabet_page(self):
        """
        Tests that user can view alphabets to choose from in a session.
        """
        response = self.client.post("/meal-sessions/start/", self.data)

        response = self.client.get("/users/?filter=A")

        self.assertEquals(response.status_code, 200)

    def test_can_view_user_page(self):
        """
        Tests that user can view list of users.
        """
        response = self.client.get("/users/")

        self.assertEquals(response.status_code, 200)

    def test_can_view_user_info(self):
        """
        Tests that priviledged user can retrieve user info securedly.
        """
        response = self.client.post(
            "/users/1/retrieve-secure/", self.passphrase)
        self.assertEquals(response.status_code, 200)
        self.assertIn("slack_id", response.content)

    def test_can_tap_breakfast(self):
        """
        Tests that user can tap for breakfast.
        """
        self.data['before_midday'] = True
        response = self.client.post("/meal-sessions/start/", self.data)
        response = self.client.post("/users/1/tap/",)
        self.assertEquals(response.status_code, 200)

    def test_can_tap_lunch(self):
        """
        Tests that user can tap for lunch.
        """
        self.data['before_midday'] = False
        response = self.client.post("/meal-sessions/start/", self.data)
        response = self.client.post("/users/1/tap/",)
        self.assertEquals(response.status_code, 200)

        self.assertEquals(response.status_code, 200)

    def test_can_untap_breakfast(self):
        """
        Tests that priviledged user can untap for breakfast.
        """
        self.data['before_midday'] = True
        response = self.client.post("/meal-sessions/start/", self.data)
        response = self.client.post("/users/1/tap/",)
        response = self.client.post("/users/1/untap/", self.passphrase)
        self.assertEquals(response.status_code, 200)

    def test_can_untap_lunch(self):
        """
        Tests that priviledged user can untap for lunch.
        """
        self.data['before_midday'] = False
        response = self.client.post("/meal-sessions/start/", self.data)
        response = self.client.post("/users/1/tap/",)
        response = self.client.post("/users/1/untap/", self.passphrase)

        self.assertEquals(response.status_code, 200)

    def test_can_nfc_tap_breakfast(self):
        """
        Tests that user can NFC tap for breakfast.
        """
        self.data['before_midday'] = True
        self.data['slackUserId'] = 'U24A2R2'
        response = self.client.post("/meal-sessions/start/", self.data)
        response = self.client.post("/users/nfctap/", self.data)
        self.assertEquals(response.status_code, 200)

    def test_can_nfc_tap_lunch(self):
        """
        Tests that user can NFC tap for lunch.
        """
        self.data['before_midday'] = False
        self.data['slackUserId'] = 'U24A2R2'
        response = self.client.post("/meal-sessions/start/", self.data)
        response = self.client.post("/users/nfctap/", self.data)
        self.assertEquals(response.status_code, 200)

    @skipUnless
    def test_can_view_reports(self):
        """
        Tests that user can view reports.
        """
        time_today = timezone.now()
        date = time_today.date()
        # Do tap.
        self.data['before_midday'] = True
        response = self.client.post("/meal-sessions/start/", self.data)
        identities = ['U24A2R1', 'U24A2R2', 'U24A2R3', 'U24A2R4']
        for identity in identities:
            self.data['slackUserId'] = identity
            response = self.client.post("/users/nfctap/", self.data)
        # Cram reports.
        response = self.client.get("/reports/")
        self.assertEquals(response.status_code, 200)
        self.assertIn('breakfast', response.content)
        self.assertIn('lunch', response.content)
        self.assertIn(str(date), response.content)
        # Cram reports for a period.
        year_month = time_today.strftime("%Y-%m")
        response = self.client.get("/reports/?from={0}".format(year_month))
        self.assertEquals(response.status_code, 200)
        self.assertIn(year_month, response.content)

    @classmethod
    def tearDownClass(cls):
        super(ServiceTestCase, cls).tearDownClass()
