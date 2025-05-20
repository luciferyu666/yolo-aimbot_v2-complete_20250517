
import socket, time
from ..packet_struct import build_packet

class NetKMBox:
    def __init__(self, host='127.0.0.1', port=7000, retries=3, timeout=0.1):
        self.addr=(host,port); self.retries=retries; self.timeout=timeout
        self._sock=self._new_sock()
    def _new_sock(self):
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.settimeout(self.timeout)
        return s
    def send(self,x,y):
        pkt=build_packet(x,y)
        for _ in range(self.retries):
            try:
                self._sock.sendto(pkt,self.addr)
                return True
            except OSError:
                self._sock=self._new_sock()
        return False
