
from control.kmbox_protocol.packet_struct import build_packet
def test_packet():
    pkt = build_packet(10,20)
    assert pkt[0]==0xAA and pkt[-1]==0x55
