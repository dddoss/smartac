# AC Controller Application

This project is designed to automate the control of a window unit air conditioner using a YoLink Wi-Fi outlet and a YoLink Wi-Fi thermometer. The application monitors the temperature and powers the air conditioner on or off based on user-defined temperature ranges.

## Project Structure

```
ac-controller-app
├── src
│   ├── main.py                # Entry point of the application
│   ├── yolink_outlet.py       # YoLinkOutlet class for outlet control
│   ├── yolink_thermometer.py  # YoLinkThermometer class for temperature readings
│   ├── yolink_token_manager.py# YoLinkUACTokenManager for UAC token handling
│   ├── yolink_device_utils.py # Utility for fetching device tokens
│   └── config.py              # Configuration settings
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ac-controller-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Before running the application, configure the `config.py` file with your YoLink UAC credentials (`secret_key`, `client_uaid`), the device IDs for your outlet and thermometer, the desired temperature range, and the polling frequency (in seconds).

### How to Find Your Device IDs and UAC Credentials

- **Device IDs:**
  1. Open the YoLink mobile app on your phone.
  2. Tap on your outlet or thermometer device.
  3. Tap the three dots (menu) in the upper right.
  4. The `Device EUI` will be shown in the details screen. Copy this value for use in your config.

- **UAC Credentials (secret_key and client_uaid):**
  1. In the YoLink app, go to "Account" > "Advanced Settings" > "User Access Credentials".
  2. Tap the plus sign to generate your `secret_key` and `client_uaid` (UAID).
  3. Copy these values for use in your config.
  4. For more details, see the [YoLink UAC Quick Start Guide](http://doc.yosmart.com/docs/overall/qsg_uac).

Example `config.py`:
```python
TEMP_RANGE = {
    "min": 70,  # Minimum desired temperature in Fahrenheit
    "max": 75   # Maximum desired temperature in Fahrenheit
}
POLLING_FREQUENCY = 300  # seconds (5 minutes)
YOLINK_OUTLET = {"device_id": "your_outlet_device_id"}
YOLINK_THERMOMETER = {"device_id": "your_thermometer_device_id"}
YOLINK_TOKENS = {
    "secret_key": "your_secret_key",
    "client_uaid": "your_client_uaid"
}
```

## Usage

To start the application, run the following command:
```
python src/main.py
```

The application will monitor the temperature and control the air conditioner based on the specified temperature range, checking every `POLLING_FREQUENCY` seconds.

## Notes
- The application uses YoLink OpenAPI V2 (UAC) for secure access.
- Device tokens are automatically fetched at startup using `Home.getDeviceList`.
- Both the outlet and thermometer require their device tokens for API calls.

## YoLink API Documentation
- [YoLink OpenAPI V2 (UAC) Documentation](http://doc.yosmart.com/docs/protocol/openAPIV2)
- [YoLink UAC Quick Start Guide](http://doc.yosmart.com/docs/overall/qsg_uac)
- [YoLink API Main Docs](http://doc.yosmart.com/docs/overall/intro)

## License

This project is licensed under the MIT License.