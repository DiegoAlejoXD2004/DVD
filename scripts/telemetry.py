import time
import curses
from pymavlink import mavutil

# Establish connection to the MAVLink device
connection = mavutil.mavlink_connection('tcp:10.13.0.3:5760')

# Wait for the first heartbeat
print("Waiting for heartbeat...")
connection.wait_heartbeat()
print("Heartbeat received from system (system %u component %u)" % (connection.target_system, connection.target_component))

def init_curses():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    return stdscr

def print_telemetry(stdscr, telemetry_data):
    stdscr.clear()
    for i, (key, value) in enumerate(telemetry_data.items()):
        stdscr.addstr(i, 0, f"{key}: {value}")
    stdscr.refresh()

def main(stdscr):
    telemetry_data = {
        "HEARTBEAT": "N/A",
        "SYS_STATUS": "N/A",
        "GPS_RAW_INT": "N/A",
        "GLOBAL_POSITION_INT": "N/A",
        "ATTITUDE": "N/A",
        "ALTITUDE": "N/A",
        "BATTERY_STATUS": "N/A",
        "VFR_HUD": "N/A",
        "STATUSTEXT": "N/A",
        "MISSION_CURRENT": "N/A",
        "NAV_CONTROLLER_OUTPUT": "N/A",
        "RADIO_STATUS": "N/A",
    }

    while True:
        msg = connection.recv_match(blocking=True)
        if msg:
            if msg.get_type() == 'HEARTBEAT':
                telemetry_data["HEARTBEAT"] = f"Type: {msg.type}, Autopilot: {msg.autopilot}, Base mode: {msg.base_mode}, System status: {msg.system_status}"
            elif msg.get_type() == 'SYS_STATUS':
                telemetry_data["SYS_STATUS"] = f"Battery voltage: {msg.voltage_battery}, Battery current: {msg.current_battery}, Battery remaining: {msg.battery_remaining}"
            elif msg.get_type() == 'GPS_RAW_INT':
                telemetry_data["GPS_RAW_INT"] = f"Lat: {msg.lat}, Lon: {msg.lon}, Alt: {msg.alt}, Satellites: {msg.satellites_visible}"
            elif msg.get_type() == 'GLOBAL_POSITION_INT':
                telemetry_data["GLOBAL_POSITION_INT"] = f"Lat: {msg.lat}, Lon: {msg.lon}, Alt: {msg.alt}, Relative Alt: {msg.relative_alt}"
                telemetry_data["ALTITUDE"] = f"Alt: {msg.alt}, Relative Alt: {msg.relative_alt}"
            elif msg.get_type() == 'ATTITUDE':
                telemetry_data["ATTITUDE"] = f"Roll: {msg.roll}, Pitch: {msg.pitch}, Yaw: {msg.yaw}"
            elif msg.get_type() == 'BATTERY_STATUS':
                telemetry_data["BATTERY_STATUS"] = f"Voltage: {msg.voltages[0]}, Current: {msg.current_battery}"
            elif msg.get_type() == 'VFR_HUD':
                telemetry_data["VFR_HUD"] = f"Airspeed: {msg.airspeed}, Groundspeed: {msg.groundspeed}, Heading: {msg.heading}"
            elif msg.get_type() == 'STATUSTEXT':
                telemetry_data["STATUSTEXT"] = f"Text: {msg.text}"
            elif msg.get_type() == 'MISSION_CURRENT':
                telemetry_data["MISSION_CURRENT"] = f"Seq: {msg.seq}"
            elif msg.get_type() == 'NAV_CONTROLLER_OUTPUT':
                telemetry_data["NAV_CONTROLLER_OUTPUT"] = f"Nav bearing: {msg.nav_bearing}, Target bearing: {msg.target_bearing}, Wp dist: {msg.wp_dist}"
            elif msg.get_type() == 'RADIO_STATUS':
                telemetry_data["RADIO_STATUS"] = f"RSSI: {msg.rssi}, Rem RSSI: {msg.remrssi}, Noise: {msg.noise}, Rem noise: {msg.remnoise}"

            print_telemetry(stdscr, telemetry_data)

# Start telemetry monitor
curses.wrapper(main)
