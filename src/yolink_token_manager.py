import requests
import time

class YoLinkUACTokenManager:
    def __init__(self, secret_key, client_uaid):
        self.secret_key = secret_key
        self.client_uaid = client_uaid
        self.token = None
        self.token_expiry = 0
        self.token_url = "http://api.yosmart.com/open/yolink/token"

    def get_token(self):
        now = int(time.time())
        if self.token and now < self.token_expiry - 60:
            return self.token
        payload = {
            "grant_type": "client_credentials",
            "client_secret": self.secret_key,
            "client_id": self.client_uaid
        }
        response = requests.post(self.token_url, params=payload)
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token")
            self.token_expiry = now + int(data.get("expires_in", 3600))
            print(f"YoLink UAC token obtained: {self.token}, expires in {self.token_expiry - now} seconds")
            return self.token
        raise Exception(f"Failed to get YoLink UAC token: {response.text}")
