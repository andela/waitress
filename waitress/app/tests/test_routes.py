from django.test import TestCase, Client
from app.models import Passphrase, SlackUser


class ServiceTestCase(TestCase):
    """
    Tests service functionality
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
        Tests that priviledged user can start a session
        """
        response = self.client.get("/meal-sessions/",)
        self.assertEquals(response.status_code, 200)

    def test_can_view_finish_session_page(self):
        """
        Tests that priviledged user can finish a session
        """
        response = self.client.post("/meal-sessions/start/", self.data)

        response = self.client.post("/meal-sessions/stop/", self.data)

        self.assertEquals(response.status_code, 200)

    def test_can_view_alphabet_page(self):
        """
        Tests that user can view alphabets to choose from in a session
        """
        response = self.client.post("/meal-sessions/start/", self.data)

        response = self.client.get("/users/?filter=A")

        self.assertEquals(response.status_code, 200)

    def test_can_view_user_page(self):
        """
        Tests that user can view list of users
        """
        response = self.client.get("/users/")

        self.assertEquals(response.status_code, 200)

    def test_can_tap_breakfast(self):
        """
        Tests that user can tap for breakfast
        """
        self.data['before_midday'] = True
        response = self.client.post("/meal-sessions/start/", self.data)
        response = self.client.post("/users/1/tap/",)
        self.assertEquals(response.status_code, 200)

        self.assertEquals(response.status_code, 200)

    def test_can_tap_lunch(self):
        """
        Tests that user can tap for lunch
        """
        self.data['before_midday'] = False
        response = self.client.post("/meal-sessions/start/", self.data)
        response = self.client.post("/users/1/tap/",)
        self.assertEquals(response.status_code, 200)

        self.assertEquals(response.status_code, 200)

    def test_can_untap_breakfast(self):
        """
        Tests that priviledged user can untap for breakfast
        """
        self.data['before_midday'] = True
        response = self.client.post("/meal-sessions/start/", self.data)
        response = self.client.post("/users/1/tap/",)
        response = self.client.post("/users/1/untap/", self.passphrase)
        self.assertEquals(response.status_code, 200)

    def test_can_untap_lunch(self):
        """
        Tests that priviledged user can untap for lunch
        """
        self.data['before_midday'] = False
        response = self.client.post("/meal-sessions/start/", self.data)
        response = self.client.post("/users/1/tap/",)
        response = self.client.post("/users/1/untap/", self.passphrase)

        self.assertEquals(response.status_code, 200)

    @classmethod
    def tearDownClass(cls):
        super(ServiceTestCase, cls).tearDownClass()
