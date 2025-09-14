import pytest
from src.aioworxmower.secrets import load_secrets
from src.aioworxmower.providers.worx import WorxProvider

pytestmark = pytest.mark.integration

@pytest.mark.asyncio
async def test_login_and_discovery():
    sec = load_secrets()
    assert sec.get("username") and sec.get("password"), "Missing credentials"
    p = WorxProvider(
        username=sec.get("username",""),
        password=sec.get("password",""),
        client_id=sec.get("client_id",""),
        client_secret=sec.get("client_secret",""),
    )
    await p.login()
    devs = await p.list_devices()
    assert isinstance(devs, list)
    boot = await p.get_bootstrap()
    assert boot.endpoint and boot.client_id
