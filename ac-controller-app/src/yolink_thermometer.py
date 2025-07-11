import requests
from yolink_token_manager import YoLinkUACTokenManager

class YoLinkThermometer:
    def __init__(self, token_manager, device_id, device_token):
        self.device_id = device_id
        self.device_token = device_token
        self.token_manager = token_manager
        self.api_url = "https://api.yosmart.com/open/yolink/v2/api"

    def get_temperature(self):
        temperature = self._fetch_temperature_from_api()
        return temperature

    def _fetch_temperature_from_api(self):
        token = self.token_manager.get_token()
        payload = {
            "method": "THSensor.getState",
            "targetDevice": self.device_id,
            "token": self.device_token
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(self.api_url, json=payload, headers=headers)
        print(f"API request payload: {payload}")  # Debugging line
        print(f"API request headers: {headers}")  # Debugging line
        print(f"API response: {response}")  

        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()
            print(f"API response: {data}")  # Debugging line
            temp_c = data.get("data", {}).get("state", {}).get("temperature")
            if temp_c is not None:
                return temp_c * 9 / 5 + 32  # Convert Celsius to Fahrenheit
        return None