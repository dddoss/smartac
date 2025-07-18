import requests
import logging

class YoLinkThermometer:
    def __init__(self, token_manager, device_id, device_token):
        self.device_id = device_id
        self.device_token = device_token
        self.token_manager = token_manager
        self.api_url = "https://api.yosmart.com/open/yolink/v2/api"

    def get_temperature(self):
        token = self.token_manager.get_token()
        if token is None:
            logging.error("YoLinkThermometer: Could not obtain access token.")
            return None
        payload = {
            "method": "THSensor.getState",
            "targetDevice": self.device_id,
            "token": self.device_token
        }
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                temp_c = data.get("data", {}).get("state", {}).get("temperature")
                if temp_c is not None:
                    return temp_c * 9 / 5 + 32  # Convert Celsius to Fahrenheit
            return None
        except Exception as e:
            logging.error(f"YoLinkThermometer get_temperature error: {e}")
            return None