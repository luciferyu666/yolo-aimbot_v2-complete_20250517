"""Integration tests for KMBox NET controller."""
import asyncio
import pytest
from backend.control.kmbox_net import discover, KMBoxNetController
from tests.integration.mock_kmbox_net_server import main as start_mock

@pytest.fixture(scope="module", autouse=True)
def mock_server():
    task = asyncio.create_task(start_mock())
    yield
    task.cancel()

@pytest.mark.asyncio
async def test_discover():
    devices = await discover(timeout=1.0)
    assert devices, "No devices discovered"

@pytest.mark.asyncio
async def test_connect_and_send():
    devices = await discover(timeout=1.0)
    ctrl = KMBoxNetController(devices[0].ip)
    await ctrl.connect()
    await ctrl.send_command(b"PING")
    await ctrl.close()
