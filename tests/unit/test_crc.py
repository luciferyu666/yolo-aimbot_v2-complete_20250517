
from control.kmbox_protocol.packet_struct import build_packet
def test_crc_len():
    pkt=build_packet(5,5)
    assert len(pkt)==6 and pkt[0]==0xAA and pkt[-1]==0x55
