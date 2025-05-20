
import socket, threading, time
from control.kmbox_protocol.net_adapter.net_client import NetKMBox
from control.kmbox_protocol.packet_struct import build_packet

def echo_server():
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(('127.0.0.1',7000))
    data,addr=s.recvfrom(1024)
    s.sendto(data,addr)
    s.close()

def test_loop():
    th=threading.Thread(target=echo_server,daemon=True); th.start()
    client=NetKMBox('127.0.0.1',7000)
    client.send(1,2)
    time.sleep(0.1)
