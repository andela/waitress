import unittest
from unittest import mock

from backup import slack_service


class SlackServiceTestCase(unittest.TestCase):
    @mock.patch("backup.slack_service.client")
    def test_send_message(self, mocked_slack_client):
        mock_response = {
            "ok": True,
            "channel": "C0J8M5QMN",
            "ts": "1503435956.000247",
            "message": {
                "text": "this is a test",
                "type": "message",
                "ts": "1503435956.000247",
            },
        }
        mocked_slack_client.chat_postMessage.return_value = mock_response

        dummy_message = "this is a test"
        resp = slack_service.send_message(dummy_message)

        mocked_slack_client.chat_postMessage.assert_called()
        self.assertEqual(resp.get("ok", False), True)
        self.assertEqual(resp.get("channel"), "C0J8M5QMN")
        message = resp.get("message")
        self.assertEqual(message.get("text"), dummy_message)


if __name__ == "__main__":
    unittest.main()
