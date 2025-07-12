import time
import json
import os
from yolink_token_manager import YoLinkUACTokenManager
from yolink_outlet import YoLinkOutlet
from yolink_thermometer import YoLinkThermometer
from yolink_device_utils import get_device_tokens

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def main():
    config = load_config()
    TEMP_RANGE = config["TEMP_RANGE"]
    POLLING_FREQUENCY = config["POLLING_FREQUENCY"]
    YOLINK_OUTLET = config["YOLINK_OUTLET"]
    YOLINK_THERMOMETER = config["YOLINK_THERMOMETER"]
    YOLINK_TOKENS = config["YOLINK_TOKENS"]

    token_manager = YoLinkUACTokenManager(
        secret_key=YOLINK_TOKENS["secret_key"],
        client_uaid=YOLINK_TOKENS["client_uaid"]
    )
    device_ids = [YOLINK_OUTLET["device_id"], YOLINK_THERMOMETER["device_id"]]
    device_tokens = get_device_tokens(device_ids, token_manager)
    outlet = YoLinkOutlet(token_manager, YOLINK_OUTLET["device_id"], device_tokens[YOLINK_OUTLET["device_id"]])
    thermometer = YoLinkThermometer(token_manager, YOLINK_THERMOMETER["device_id"], device_tokens[YOLINK_THERMOMETER["device_id"]])

    while True:
        config = load_config()
        TEMP_RANGE = config["TEMP_RANGE"]
        POLLING_FREQUENCY = config["POLLING_FREQUENCY"]

        current_temperature = thermometer.get_temperature()
        print(f"Current temperature: {current_temperature} F")

        if current_temperature is None:
            print("Failed to read temperature.")
        elif current_temperature < TEMP_RANGE['min']:
            print("Temperature below range. Turning OFF AC.")
            outlet.power_off()
        elif current_temperature > TEMP_RANGE['max']:
            print("Temperature above range. Turning ON AC.")
            outlet.power_on()
        else:
            print("Temperature within range. No action taken.")

        print(f"Waiting {POLLING_FREQUENCY} seconds before next check...")
        time.sleep(POLLING_FREQUENCY)

if __name__ == "__main__":
    main()