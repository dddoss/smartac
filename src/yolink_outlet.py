import requests
from yolink_token_manager import YoLinkUACTokenManager

class YoLinkOutlet:
    def __init__(self, token_manager, device_id, device_token):
        self.device_id = device_id
        self.device_token = device_token
        self.token_manager = token_manager
        self.api_url = "https://api.yosmart.com/open/yolink/v2/api"

    def power_on(self):
        token = self.token_manager.get_token()
        payload = {
            "method": "Outlet.setState",
            "targetDevice": self.device_id,
            "token": self.device_token,
            "params": {"state": "open"}
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(self.api_url, json=payload, headers=headers)
        return response.status_code == 200

    def power_off(self):
        token = self.token_manager.get_token()
        payload = {
            "method": "Outlet.setState",
            "targetDevice": self.device_id,
            "token": self.device_token,
            "params": {"state": "closed"}
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(self.api_url, json=payload, headers=headers)
        return response.status_code == 200

    def get_status(self):
        token = self.token_manager.get_token()
        payload = {
            "method": "Outlet.getState",
            "targetDevice": self.device_id,
            "token": self.device_token
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(self.api_url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("state", {}).get("state")
        return None
