import asyncio, pytest
from src.aioworxmower.secrets import load_secrets
from src.aioworxmower.session import MowerSession

pytestmark = pytest.mark.integration

@pytest.mark.asyncio
async def test_realtime_subscribe():
    sec = load_secrets()
    assert sec.get("username") and sec.get("password"), "Missing credentials"
    sess = MowerSession(
        username=sec.get("username",""),
        password=sec.get("password",""),
        client_id=sec.get("client_id",""),
        client_secret=sec.get("client_secret",""),
    )
    await sess.connect()
    dev = sess.get_device()
    assert dev.topic_status
    await asyncio.sleep(2)
    await sess.disconnect()
