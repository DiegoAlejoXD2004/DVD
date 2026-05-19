'''
How to view max radium of a cilyndrical way
'''
from pymavlink import mavutil

connection = mavutil.mavlink_connection("tcp:10.13.0.3:5760")

connection.wait_heartbeat()

target_system = connection.target_system
target_component = connection.target_component

connection.mav.param_request_read_send(
    target_system,
    target_component,
    b"FENCE_RADIUS",
    -1
)

msg = connection.recv_match(type="PARAM_VALUE", blocking=True, timeout=5)

if msg is not None and msg.param_id.strip("\x00") == "FENCE_RADIUS":
    print(f"Valor actual de FENCE_RADIUS: {msg.param_value}")
else:
    print("No se recibió el valor de FENCE_RADIUS")
