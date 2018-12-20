import requests
import json
import os


def send_slack_message(message, slack_webhook_url=os.environ['slack_webhook_url'], slack_channel_name = os.environ['slack_channel_name']):
    message_dict = {'text': message,
                    'username': u'rundeck script',
                    'icon_emoji': u':ghost:',
                    'channel': slack_channel_name,
                    'link_names': 1,
                    }
    requests.post(slack_webhook_url, data=json.dumps(message_dict))
