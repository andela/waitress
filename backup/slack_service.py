class SlackService:
    """SlackService allows communication with Slack."""

    def __init__(self, client, channel):
        self.client = client
        self.channel = channel

    def send_message(self, message):
        if self.client is None:
            return print(message)
        return self.client.chat_postMessage(channel=self.channel, text=message)
