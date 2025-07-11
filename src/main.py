import time
from config import TEMP_RANGE, YOLINK_OUTLET, YOLINK_THERMOMETER, YOLINK_TOKENS, POLLING_FREQUENCY
from yolink_token_manager import YoLinkUACTokenManager
from yolink_outlet import YoLinkOutlet
from yolink_thermometer import YoLinkThermometer
from yolink_device_utils import get_device_tokens

def main():
    # Initialize shared token manager (UAC)
    token_manager = YoLinkUACTokenManager(
        secret_key=YOLINK_TOKENS["secret_key"],
        client_uaid=YOLINK_TOKENS["client_uaid"]
    )

    # Get device tokens for outlet and thermometer
    device_ids = [YOLINK_OUTLET["device_id"], YOLINK_THERMOMETER["device_id"]]
    device_tokens = get_device_tokens(device_ids, token_manager)

    outlet = YoLinkOutlet(token_manager, YOLINK_OUTLET["device_id"], device_tokens[YOLINK_OUTLET["device_id"]])
    thermometer = YoLinkThermometer(token_manager, YOLINK_THERMOMETER["device_id"], device_tokens[YOLINK_THERMOMETER["device_id"]])

    while True:
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