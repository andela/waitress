import unittest

from backup.slack_service import SlackService, make_slack_client


def fake_chat_post_message(**kwargs):
    return {
        "ok": True,
        "channel": "C0J8M5QMN",
        "ts": "1503435956.000247",
        "message": {
            "text": "this is a test",
            "type": "message",
            "ts": "1503435956.000247",
        },
    }


class SlackServiceTestCase(unittest.TestCase):
    def test_send_message(self):
        client = make_slack_client(fake_chat_post_message)
        slack_service = SlackService(client, "C0J8M5QMN")

        dummy_message = "this is a test"
        resp = slack_service.send_message(dummy_message)

        self.assertEqual(resp.get("ok", False), True)
        self.assertEqual(resp.get("channel"), "C0J8M5QMN")
        message = resp.get("message")
        self.assertEqual(message.get("text"), dummy_message)


if __name__ == "__main__":
    unittest.main()
