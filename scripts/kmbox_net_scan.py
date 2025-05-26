"""CLI for KMBox NET discovery.

Usage:
    python scripts/kmbox_net_scan.py
"""
import asyncio
from backend.control.kmbox_net import discover

async def main():
    devices = await discover()
    if devices:
        print("Discovered devices:")
        for d in devices:
            print(f"- {d.ip} ({d.hw_id})")
    else:
        print("No KMBox NET devices found.")

if __name__ == "__main__":
    asyncio.run(main())
