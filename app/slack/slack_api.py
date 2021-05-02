import requests

class SlackApi:
    POST_URL = "https://slack.com/api/chat.postMessage"

    def __init__(self, api_key):
        self.api_key = api_key
    
    def post_message(self, message):
        form_data = dict(
            channel="U01NAHQC62H",
            text=message
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        response = requests.post(SlackApi.POST_URL, headers=headers, data=form_data)
        pass