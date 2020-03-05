import unittest
from unittest import mock

from backup.slack_service import SlackService


class SlackServiceTestCase(unittest.TestCase):
    def test_send_message(self):
        mock_client = mock.Mock()
        mock_client.chat_postMessage.return_value = {
            "ok": True,
            "channel": "C0J8M5QMN",
            "ts": "1503435956.000247",
            "message": {
                "text": "this is a test",
                "type": "message",
                "ts": "1503435956.000247",
            },
        }
        slack_service = SlackService(mock_client, "C0J8M5QMN")
        dummy_message = "this is a test"
        resp = slack_service.send_message(dummy_message)

        self.assertEqual(resp.get("ok", False), True)
        self.assertEqual(resp.get("channel"), "C0J8M5QMN")
        message = resp.get("message")
        self.assertEqual(message.get("text"), dummy_message)


if __name__ == "__main__":
    unittest.main()
