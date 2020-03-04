import os

from dotenv import find_dotenv, load_dotenv
from slack import WebClient

load_dotenv(find_dotenv())

client = WebClient(token=os.getenv("SLACK_API_TOKEN"))


def send_message(message):
    return client.chat_postMessage(channel="C0J8M5QMN", text=message)
