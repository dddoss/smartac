# Example configuration for the AC Controller App.
# Fill this file with your specific configuration details, and then rename it to `config.py`.

TEMP_RANGE = {
    "min": 70,  # Minimum desired temperature in Fahrenheit
    "max": 72   # Maximum desired temperature in Fahrenheit
}

POLLING_FREQUENCY = 300  # seconds (5 minutes)

# YoLink UAC credentials for Outlet
YOLINK_OUTLET = {
    "device_id": "your_device_id"
}

# YoLink UAC credentials for Thermometer
YOLINK_THERMOMETER = {
    "device_id": "your_device_id"
}

YOLINK_TOKENS = {
    "secret_key": 'your_secret_key',
    "client_uaid": 'your_client_uaid',
}