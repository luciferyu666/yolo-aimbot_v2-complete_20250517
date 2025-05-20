
from .crc8 import crc8
def build_payload(x:int,y:int,btn:int=1): return bytes([x&0xFF,y&0xFF,btn&0xFF])
def build_packet(x:int,y:int,btn:int=1):
    payload=build_payload(x,y,btn)
    return bytes([0xAA])+payload+bytes([crc8(payload)])+bytes([0x55])
