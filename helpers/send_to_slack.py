#!/user/bin/env python3.6

import os

from slackclient import SlackClient

SLACK_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
CHANNEL = os.environ.get('SLACK_CHANNEL')
CLIENT = SlackClient(SLACK_TOKEN)

def message_to_slack(message, channel=CHANNEL):
    CLIENT.api_call(
        'chat.postMessage',
        channel=channel,
        text=message,
    )
