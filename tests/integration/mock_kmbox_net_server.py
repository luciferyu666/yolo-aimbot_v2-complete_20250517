"""A minimal async mock server to emulate KMBox NET responses."""
import asyncio
import socket

DISCOVERY_PORT = 5959
COMMAND_PORT = 5960
DISCOVERY_MAGIC = b"KMBOX_DISCOVERY"

async def discovery_responder():
    loop = asyncio.get_running_loop()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    sock.bind(("", DISCOVERY_PORT))
    while True:
        data, addr = await loop.sock_recvfrom(sock, 1024)
        if data == DISCOVERY_MAGIC:
            await loop.sock_sendto(sock, b"MOCK_HW_ID", addr)

async def command_server():
    server = await asyncio.start_server(lambda r, w: None, "0.0.0.0", COMMAND_PORT)
    async with server:
        await server.serve_forever()

async def main():
    await asyncio.gather(discovery_responder(), command_server())

if __name__ == "__main__":
    asyncio.run(main())
