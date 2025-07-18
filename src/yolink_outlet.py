import requests
from yolink_token_manager import YoLinkUACTokenManager
import logging

class YoLinkOutlet:
    def __init__(self, token_manager, device_id, device_token):
        self.device_id = device_id
        self.device_token = device_token
        self.token_manager = token_manager
        self.api_url = "https://api.yosmart.com/open/yolink/v2/api"

    def power_on(self):
        token = self.token_manager.get_token()
        if token is None:
            logging.error("YoLinkOutlet: Could not obtain access token.")
            return False
        payload = {
            "method": "Outlet.setState",
            "targetDevice": self.device_id,
            "token": self.device_token,
            "params": {"state": "open"}
        }
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            return response.status_code == 200
        except Exception as e:
            logging.error(f"YoLinkOutlet power_on error: {e}")
            return False

    def power_off(self):
        if self.token_manager is None:
            logging.error("YoLinkOutlet: token_manager is None. Cannot power off.")
            return False
        token = self.token_manager.get_token()
        if token is None:
            logging.error("YoLinkOutlet: Could not obtain access token.")
            return False
        payload = {
            "method": "Outlet.setState",
            "targetDevice": self.device_id,
            "token": self.device_token,
            "params": {"state": "closed"}
        }
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            return response.status_code == 200
        except Exception as e:
            logging.error(f"YoLinkOutlet power_off error: {e}")
            return False

    def get_status(self):
        if self.token_manager is None:
            logging.error("YoLinkOutlet: token_manager is None. Cannot get status.")
            return None
        token = self.token_manager.get_token()
        if token is None:
            logging.error("YoLinkOutlet: Could not obtain access token.")
            return None
        payload = {
            "method": "Outlet.getState",
            "targetDevice": self.device_id,
            "token": self.device_token
        }
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data.get("data", {}).get("state", {}).get("state")
            return None
        except Exception as e:
            logging.error(f"YoLinkOutlet get_status error: {e}")
            return None
