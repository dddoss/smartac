import requests
import time

def get_device_tokens(device_ids, token_manager):   
    """
    Fetch device tokens for the given device_ids using Home.getDeviceList.
    Returns a dict mapping device_id to device_token.
    """
    # Get UAC access token
    access_token = token_manager.get_token()
    url = "http://api.yosmart.com/open/yolink/v2/api"
    payload = {
        "method": "Home.getDeviceList",
        "time": time.time(),
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to get device list: {response.text}")
    data = response.json()
    device_tokens = {}
    for device in data.get("data", {}).get("devices", []):
        if device["deviceId"] in device_ids:
            device_tokens[device["deviceId"]] = device.get("token")
    print(f"Device tokens obtained: {device_tokens}")
    return device_tokens
