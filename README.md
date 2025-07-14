# SmartAC Controller

A Python application to control a window unit air conditioner using YoLink WiFi outlet and thermometer, with support for scheduled temperature ranges.

## Features

- Supports multiple temperature schedules per day (UTC, HH:MM format).
- Reads configuration from `config.json` on every polling loop (change temperature or polling frequency without restart).
- Uses YoLink OpenAPI V2 (UAC) for secure device control.
- Graceful handling of disabled schedules and overlapping schedule detection.

## Configuration

1. **Copy and edit the example config:**

   ```sh
   cp src/example_config.json src/config.json
   ```

2. **Edit `src/config.json`:**

   - Fill in your YoLink device IDs and UAC credentials (see below).
   - Define your desired schedules in the `SCHEDULES` array.
   - Only changes to `SCHEDULES.TEMP_RANGE` and `POLLING_FREQUENCY` take effect without restart.

   Example:
   ```json
   {
     "SCHEDULES": [
       {
         "START_TIME": "00:00",
         "END_TIME": "08:00",
         "TEMP_RANGE": { "min": 72, "max": 74 },
         "ENABLE": true
       },
       {
         "START_TIME": "08:00",
         "END_TIME": "18:00",
         "TEMP_RANGE": { "min": 75, "max": 78 }
       },
       {
         "START_TIME": "18:00",
         "END_TIME": "23:59",
         "TEMP_RANGE": { "min": 70, "max": 72 },
         "ENABLE": false
       }
     ],
     "POLLING_FREQUENCY": 300,
     "YOLINK_OUTLET": {
       "device_id": "your_outlet_device_id"
     },
     "YOLINK_THERMOMETER": {
       "device_id": "your_thermometer_device_id"
     },
     "YOLINK_TOKENS": {
       "secret_key": "your_secret_key",
       "client_uaid": "your_client_uaid"
     }
   }
   ```

## How to Find Your Device IDs and UAC Credentials

- **Device IDs:**  
  Open the YoLink app, select your device, and look for the Device ID in the device details.

- **UAC Credentials (secret key and client uaid):**  
  In the YoLink app, go to Account > Developer Center > User Authorization Code (UAC).  
  Copy your `client_uaid` and `secret_key` from there.

## Schedule Rules

- Schedules use UTC time in `HH:MM` format.
- If schedules overlap, the program logs an error and exits.
- If a schedule has `"ENABLE": false`, the outlet is always turned off during that period.
- If there are empty periods, the previous schedule's setting continues.

## Running

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

2. Run the controller:
   ```sh
   python src/main.py
   ```

## API Documentation

- [YoLink OpenAPI V2 Docs](http://doc.yosmart.com/docs/protocol/openAPIV2)
- [YoLink UAC Quick Start Guide](http://doc.yosmart.com/docs/overall/qsg_uac)
- [YoLink API Overview](http://doc.yosmart.com/docs/overall/intro/)

## License

This project is licensed under the MIT License.