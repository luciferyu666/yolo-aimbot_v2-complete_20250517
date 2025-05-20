
import serial, time
from ..packet_struct import build_packet
class SerialKMBox:
    def __init__(self, port='/dev/ttyUSB0', baud=115200, retries=3):
        self.port=port; self.baud=baud; self.retries=retries
        self._open()
    def _open(self):
        self.ser = serial.Serial(self.port,self.baud,timeout=1)
    def send(self,x,y):
        pkt=build_packet(x,y)
        for _ in range(self.retries):
            try:
                self.ser.write(pkt); return True
            except serial.SerialException:
                time.sleep(0.1); self._open()
        return False
