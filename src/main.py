import json
import time
import logging
from datetime import datetime, time as dt_time
try:
    from zoneinfo import ZoneInfo
except ImportError:
    try:
        from backports.zoneinfo import ZoneInfo
    except ImportError:
        ZoneInfo = None
import tzdata
from yolink_token_manager import YoLinkUACTokenManager
from yolink_device_utils import get_device_tokens
from yolink_thermometer import YoLinkThermometer
from yolink_outlet import YoLinkOutlet

CONFIG_PATH = "src/config.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

def load_config():
    with open(CONFIG_PATH, "r") as f:
        # Remove comments if present (JSON5 not supported by json module)
        lines = [line for line in f if not line.strip().startswith("//")]
        return json.loads("".join(lines))

def parse_time(tstr):
    return dt_time.fromisoformat(tstr)

def validate_schedules(schedules):
    # Check for overlapping schedules
    intervals = []
    for idx, sched in enumerate(schedules):
        start = parse_time(sched["START_TIME"])
        end = parse_time(sched["END_TIME"])
        intervals.append((start, end, idx))
    # Sort by start time
    intervals.sort()
    for i in range(1, len(intervals)):
        prev_end = intervals[i-1][1]
        curr_start = intervals[i][0]
        if curr_start < prev_end:
            logging.error(f"Schedule overlap detected between entries {intervals[i-1][2]} and {intervals[i][2]}.")
            return False
    return True

def get_now_local(config):
    tz_name = config.get("TIMEZONE", "Etc/Greenwich")
    if ZoneInfo:
        tz = ZoneInfo(tz_name)
        now = datetime.now(tz)
    else:
        if tz_name != "UTC":
            logging.warning("Timezone support requires Python 3.9+ (zoneinfo). Defaulting to UTC.")
        now = datetime.utcnow()
    return now.time()

def get_active_schedule(schedules, now_utc, last_schedule=None):
    # now_utc: datetime.time
    # Returns the current schedule, or the most recent previous schedule if none match
    sorted_scheds = sorted(schedules, key=lambda s: parse_time(s["START_TIME"]))
    for sched in sorted_scheds:
        start = parse_time(sched["START_TIME"])
        end = parse_time(sched["END_TIME"])
        if start <= now_utc < end:
            return sched
    # If no schedule matches, return the most recent previous schedule (by END_TIME)
    prev_scheds = [s for s in sorted_scheds if parse_time(s["END_TIME"]) <= now_utc]
    if prev_scheds:
        return prev_scheds[-1]
    # If now_utc is before the first schedule, wrap around to the last schedule (for overnight schedules)
    if sorted_scheds:
        return sorted_scheds[-1]
    # If still none, return the last schedule from previous loop (if provided)
    return last_schedule

def main():
    config = load_config()
    schedules = config.get("SCHEDULES")
    if not schedules:
        logging.error("No SCHEDULES defined in config.json. Exiting.")
        exit(1)

    token_manager = YoLinkUACTokenManager(config["YOLINK_TOKENS"]["secret_key"], config["YOLINK_TOKENS"]["client_uaid"])

    outlet_id = config["YOLINK_OUTLET"]["device_id"]
    thermometer_id = config["YOLINK_THERMOMETER"]["device_id"]
    tokens = get_device_tokens([outlet_id, thermometer_id], token_manager)

    
    # Device token retrieval logic here (omitted for brevity)
    thermometer = YoLinkThermometer(token_manager, thermometer_id, tokens[thermometer_id])
    outlet = YoLinkOutlet(token_manager, outlet_id, tokens[outlet_id])

    logging.info("SmartAC controller started.")
    last_schedule = None
    while True:
        config = load_config()
        polling_frequency = config.get("POLLING_FREQUENCY", 300)

        schedules = config.get("SCHEDULES")
        valid = validate_schedules(schedules)
        now_local = get_now_local(config)
        sched = get_active_schedule(schedules, now_local, last_schedule)
        if not valid:
            logging.error("Schedule validation failed. Turning outlet OFF.")
            outlet.power_off()
            time.sleep(polling_frequency)
            continue
        if sched is None:
            logging.info("No schedule found. Turning outlet OFF.")
            outlet.power_off()
            time.sleep(polling_frequency)
            continue
        last_schedule = sched

        if sched.get("ENABLE", True) is False:
            logging.info("Current schedule is disabled (ENABLE=false). Turning outlet OFF.")
            outlet.power_off()
            time.sleep(polling_frequency)
            continue

        temp_min = sched["TEMP_RANGE"]["min"]
        temp_max = sched["TEMP_RANGE"]["max"]
        temp = thermometer.get_temperature()
        logging.info(f"Current temperature: {temp}°F, Schedule: {sched['START_TIME']}-{sched['END_TIME']} ({temp_min}-{temp_max}°F)")
        if temp is not None:
            if temp > temp_max:
                logging.info("Turning outlet ON.")
                outlet.power_on()
            elif temp < temp_min:
                logging.info("Turning outlet OFF.")
                outlet.power_off()
        else:
            logging.warning("Could not read temperature.")
        logging.info(f"Sleeping for {polling_frequency} seconds.")
        time.sleep(polling_frequency)

if __name__ == "__main__":
    main()