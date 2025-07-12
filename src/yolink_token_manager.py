import requests
import time

class YoLinkUACTokenManager:
    def __init__(self, secret_key, client_uaid):
        self.secret_key = secret_key
        self.client_uaid = client_uaid
        self.token = None
        self.refresh_token = None
        self.token_expiry = 0
        self.token_url = "https://api.yosmart.com/open/yolink/token"

    def get_token(self):
        now = int(time.time())
        if self.token and now < self.token_expiry - 60:
            return self.token
        if self.refresh_token:
            print("Using refresh token to obtain YoLink UAC token.")
            # Use refresh_token to get a new access token
            payload = {
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
                "client_id": self.client_uaid
            }
        else:
            print("Using client credentials to obtain YoLink UAC token for the first time.")
            # Use client credentials for the first time
            payload = {
                "grant_type": "client_credentials",
                "client_secret": self.secret_key,
                "client_id": self.client_uaid
            }
        response = requests.post(self.token_url, data=payload)
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token")
            self.token_expiry = now + int(data.get("expires_in", 3600))
            if "refresh_token" in data:
                self.refresh_token = data["refresh_token"]
            print(f"YoLink UAC token successfully obtained, expires in {self.token_expiry - now} seconds.")
            return self.token
        raise Exception(f"Failed to get YoLink UAC token: {response.text}")
