from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class ServiceTestCase(TestCase):
    '''Tests service functionality '''
    def setUpClass(cls):
        cls.client = Client()
        super(ServiceTestCase, cls).setUpClass()

    def test_can_view_start_session_page(self):
        '''Tests that priviledged user can start a session'''
        response = self.client.get(reverse('start_session'))
        self.assertEquals(response.status_code, 200)

    def test_can_view_finish_session_page(self):
        '''Tests that priviledged user can finish a session'''
        pass

    def test_can_view_alphabet_page(self):
        '''Tests that user can view alphabets to choose from in a session'''
        pass

    def test_can_view_user_page(self):
        '''Tests that user can view list of users'''
        pass

    def test_can_tap_breakfast(self):
        '''Tests that user can tap for breakfast'''
        pass

    def test_can_tap_lunch(self):
        '''Tests that user can tap for lunch'''
        pass

    def test_can_untap_breakfast(self):
        '''Tests that priviledged user can untap for breakfast'''
        pass

    def test_can_untap_lunch(self):
        '''Tests that priviledged user can untap for lunch'''
        pass

    def test_can_view_users(self):
        '''Tests that user list can retrieved from slack'''
        pass

    def tearDownClass(cls):
        super(ServiceTestCase, cls).tearDownClass()
