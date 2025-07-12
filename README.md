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
│   └── config.json            # Configuration settings
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

The application uses a JSON config file at `src/config.json` for runtime settings. An example config is provided as `src/example_config.json`.

- Only `TEMP_RANGE` and `POLLING_FREQUENCY` changes take effect without restart.
- All other changes require restarting the application.
- **Do not commit your `config.json`!** It is ignored by `.gitignore`.

### Example `src/example_config.json`
```json
{
  "TEMP_RANGE": { "min": 70, "max": 75 },
  "POLLING_FREQUENCY": 60,
  "YOLINK_OUTLET": {
    "device_id": "YOUR_OUTLET_DEVICE_ID"
  },
  "YOLINK_THERMOMETER": {
    "device_id": "YOUR_THERMOMETER_DEVICE_ID"
  },
  "YOLINK_TOKENS": {
    "secret_key": "YOUR_SECRET_KEY",
    "client_uaid": "YOUR_CLIENT_UAID"
  }
}
```

- Copy `src/example_config.json` to `src/config.json` and fill in your device IDs and credentials.
- See comments in the example for which fields are hot-reloadable.

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