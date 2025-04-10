import struct
import time
import serial
import copy

from dout_common.do_mod.packets.get_do import GetDoutsRequest
from dout_common.do_mod.packets.get_do import GetDoutsResponse
from dout_common.do_mod.packets.set_do import SetDoutsRequest
from dout_common.do_mod.packets.set_do import SetDoutsResponse
from dout_common.do_mod.packets import Request
from dout_common.do_mod.packets import Response


class DigitalOutputs:
    ALL = {i: True for i in range(10)}
    NONE = {i: False for i in range(10)}

    THIRD = copy.deepcopy(NONE)
    THIRD[2] = True

    THIRD_FOURTH = copy.deepcopy(THIRD)
    THIRD_FOURTH[3] = True

    THIRD_FOURTH_EIGHTH = copy.deepcopy(THIRD_FOURTH)
    THIRD_FOURTH_EIGHTH[7] = True



def binary(dopins: dict):
    binary = 0
    for i in range(len(dopins)):
        binary |= dopins[i] << i
    return binary & 0x3FF

def digital_out_set_state(digital_out_state: dict):
    print("Setting DO state...")
    binary_state = binary(digital_out_state)
    set_req = SetDoutsRequest(binary_state)
    base_id = Request.SetDouts(set_req).base_id()
    cmd = Request.SetDouts(set_req).cmd()

    print(hex(base_id), hex(cmd), bin(binary_state))

    # TODO: packaging from Rust
    payload: int = (base_id << 11*8) | (0x7 << 7*8) | cmd << 6*8 | (0x1 << 2*8 ) | binary_state
    print(bin(payload))

    return payload.to_bytes((payload.bit_length() + 7) // 8, byteorder='big')

def digital_out_get_state():
    print("Getting DO state...")
    get_req = GetDoutsRequest()
    base_id = Request.GetDouts(get_req).base_id()
    cmd = Request.GetDouts(get_req).cmd()

    print(hex(base_id), hex(cmd))

    # TODO: packaging from Rust
    payload: int = (base_id << 11*8) | (0x7 << 7*8) | cmd << 6*8 | (0x1 << 2*8 )
    print(bin(payload))

    return payload.to_bytes((payload.bit_length() + 7) // 8, byteorder='big')

# def digital_out_read_state():
#     """
#     Read the digital out module pin state with the specified serial id.
#     :return: A 16-bit integer (0 to 65535) representing those booleans
#     """

#     payload = (cmd_dict["BASE_ID"] << 9*8) | (0x7 << 5*8) | (cmd_dict["SetDouts"] << 4*8) | 0x1
#     packed_payload = struct.pack(">BLBL", cmd_dict["BASE_ID"], 0x5, cmd_dict["GetDouts"], 0x1)  # Pack as big endian
#     print(packed_payload)

#     return packed_payload

def set_state(do_state):
    with serial.Serial("/dev/ttyACM0",timeout=1) as ser:
        msg = digital_out_set_state(do_state)
        ser.write(msg)
        responses = ser.readlines()
        for res in responses:
            print(res.decode().strip())

def get_state():
    with serial.Serial("/dev/ttyACM0",timeout=1) as ser:
        msg = digital_out_get_state()
        ser.write(msg)
        responses = ser.readlines()
        for res in responses:
            print(res.decode().strip())

if __name__ == '__main__':
    set_state(DigitalOutputs.NONE)
    get_state()