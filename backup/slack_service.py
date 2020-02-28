import os

from dotenv import find_dotenv, load_dotenv
from slack import WebClient

load_dotenv(find_dotenv())

client = WebClient(token=os.getenv("SLACK_API_TOKEN"))


def send_message(message):
    channel = os.getenv("SLACK_CHANNEL")
    return client.chat_postMessage(channel=channel, text=message)
