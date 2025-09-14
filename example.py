import asyncio
from src.aioworxmower.secrets import load_secrets
from src.aioworxmower.providers.worx import WorxProvider

async def main():
    sec = load_secrets()
    p = WorxProvider(
        username=sec.get("username",""),
        password=sec.get("password",""),
        client_id=sec.get("client_id",""),
        client_secret=sec.get("client_secret",""),
    )
    await p.login()
    devs = await p.list_devices()
    boot = await p.get_bootstrap()
    print("Bootstrap endpoint:", boot.endpoint)
    print("ClientId:", boot.client_id)
    print("Devices:")
    for d in devs:
        print("-", d.serial, d.name, d.model, d.topics)

if __name__ == "__main__":
    asyncio.run(main())
