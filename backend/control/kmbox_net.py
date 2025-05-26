"""KMBox NET (Ethernet) device controller.

Provides async socket IO helpers for command dispatch and
UDP broadcast discovery.

NOTE: Replace placeholders with actual protocol according to
KMBox NET Integration Guide.
"""

import asyncio
import socket
from dataclasses import dataclass
from typing import Optional

DISCOVERY_PORT = 5959
COMMAND_PORT = 5960
DISCOVERY_MAGIC = b"KMBOX_DISCOVERY"

@dataclass
class DeviceInfo:
    ip: str
    hw_id: str

class KMBoxNetController:
    """Async controller for a single KMBox NET device."""

    def __init__(self, ip: str, port: int = COMMAND_PORT) -> None:
        self.ip = ip
        self.port = port
        self._writer: Optional[asyncio.StreamWriter] = None
        self._reader: Optional[asyncio.StreamReader] = None

    async def connect(self):
        self._reader, self._writer = await asyncio.open_connection(self.ip, self.port)

    async def send_command(self, payload: bytes):
        if not self._writer:
            raise RuntimeError("Not connected")
        self._writer.write(payload)
        await self._writer.drain()

    async def close(self):
        if self._writer:
            self._writer.close()
            await self._writer.wait_closed()

async def discover(timeout: float = 2.0) -> list[DeviceInfo]:
    """Broadcast discovery packets and collect responses."""
    loop = asyncio.get_running_loop()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", 0))
    sock.sendto(DISCOVERY_MAGIC, ("255.255.255.255", DISCOVERY_PORT))

    devices: list[DeviceInfo] = []

    end = loop.time() + timeout
    while loop.time() < end:
        try:
            data, addr = await asyncio.wait_for(loop.sock_recvfrom(sock, 1024), timeout=end - loop.time())
            devices.append(DeviceInfo(ip=addr[0], hw_id=data.decode(errors="ignore")))
        except asyncio.TimeoutError:
            break
    sock.close()
    return devices
