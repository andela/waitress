import os

import slack


class FakeWebClient:
    """Fake slack WebClient"""
    def __init__(self, post_message):
        self.post_message = post_message

    def chat_postMessage(self, **kwargs):
        return self.post_message(**kwargs)


def make_slack_client(chat_post_message=None):
    if os.getenv("SLACK_API_TOKEN", "") == "":
        print("using fake slack client, SLACK_API_TOKEN not set")
        return FakeWebClient(chat_post_message)
    return slack.WebClient(token=os.getenv("SLACK_API_TOKEN"))


class SlackService:
    """SlackService allows communication with Slack."""
    def __init__(self, client, channel):
        self.client = client
        self.channel = channel

    def send_message(self, message):
        return self.client.chat_postMessage(channel=self.channel, text=message)
