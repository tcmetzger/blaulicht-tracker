#!/user/bin/env python3.6

import os

from slackclient import SlackClient

SLACK_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
CHANNEL = os.environ.get('SLACK_CHANNEL')
CLIENT = SlackClient(SLACK_TOKEN)

def create_attachment(story):
    """
    Create attachment info for slack
    Return attachment
    """
    #print(f'++++++++++++++++++++++++++++++++slack function: {story}')
    attached = [
        {
            'fallback': f'Vorschaubild',
            'color': '#162486',
            'title': story['media']['image'][0]['caption'],
            'text': story['title'],
            'image_url': story['media']['image'][0]['url'],
            'callback_id': story['id'],
            'footer': 'Vorschaubild:',
        }
    ]
    print(attached)
    return attached

def message_to_slack(message, attached='none', channel=CHANNEL):
    """
    Send message (with attachment, if provided), to slack channel
    Return send status
    """
    if not attached == 'none':
        print('with attachment')
        return CLIENT.api_call(
            'chat.postMessage',
            channel=channel,
            text=message,
            attachments = attached,
        )
    else:
        print('NOT with attachment')
        return CLIENT.api_call(
            'chat.postMessage',
            channel=channel,
            text=message,
        )
