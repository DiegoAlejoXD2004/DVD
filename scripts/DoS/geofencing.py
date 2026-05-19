from pymavlink import mavutil
from scapy.all import *
import sys
import socket

def set_param(mav, param_id, param_value, param_type):
    return mav.param_set_encode(
        target_system=mav.target_system,
        target_component=mav.target_component,
        param_id=param_id.encode('utf-8'),
        param_value=param_value,
        param_type=param_type
    ).pack(mav)

def send_mavlink_packet_tcp(packet_data, target_ip, target_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, target_port))
    sock.send(packet_data)
    sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python geo-fencing.py <ip:port> <action>")
        print("Actions: disable, enable, set_radius:<value>, set_alt_max:<value>, set_action:<value>")
        sys.exit(1)

    target = sys.argv[1]
    action = sys.argv[2]
    target_ip, target_port = target.split(':')
    target_port = int(target_port)

    mav = mavutil.mavlink.MAVLink(None)
    mav.target_system = 1
    mav.target_component = 1

    if action == "disable":
        packet = set_param(mav, 'FENCE_ENABLE', 0, mavutil.mavlink.MAV_PARAM_TYPE_UINT8)
        send_mavlink_packet_tcp(packet, target_ip, target_port)
        print("Geofence disabled")
    elif action == "enable":
        packet = set_param(mav, 'FENCE_ENABLE', 1, mavutil.mavlink.MAV_PARAM_TYPE_UINT8)
        send_mavlink_packet_tcp(packet, target_ip, target_port)
        print("Geofence enabled")
    elif action.startswith("set_radius:"):
        value = float(action.split(":")[1])
        packet = set_param(mav, 'FENCE_ENABLE', 1, mavutil.mavlink.MAV_PARAM_TYPE_UINT8)
        send_mavlink_packet_tcp(packet, target_ip, target_port)
        packet = set_param(mav, 'FENCE_RADIUS', value, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
        send_mavlink_packet_tcp(packet, target_ip, target_port)
        print(f"Geofence radius set to {value} meters")
    elif action.startswith("set_alt_max:"):
        value = float(action.split(":")[1])
        packet = set_param(mav, 'FENCE_ENABLE', 1, mavutil.mavlink.MAV_PARAM_TYPE_UINT8)
        send_mavlink_packet_tcp(packet, target_ip, target_port)
        packet = set_param(mav, 'FENCE_ALT_MAX', value, mavutil.mavlink.MAV_PARAM_TYPE_REAL32)
        send_mavlink_packet_tcp(packet, target_ip, target_port)
        print(f"Geofence maximum altitude set to {value} meters")
    elif action.startswith("set_action:"):
        value = int(action.split(":")[1])
        packet = set_param(mav, 'FENCE_ENABLE', 1, mavutil.mavlink.MAV_PARAM_TYPE_UINT8)
        send_mavlink_packet_tcp(packet, target_ip, target_port)
        packet = set_param(mav, 'FENCE_ACTION', value, mavutil.mavlink.MAV_PARAM_TYPE_UINT8)
        send_mavlink_packet_tcp(packet, target_ip, target_port)
        print(f"Geofence breach action set to {value}")
    else:
        print("Invalid action. Actions: disable, enable, set_radius:<value>, set_alt_max:<value>, set_action:<value>")
        sys.exit(1)
