import asyncio
from src.aioworxmower.secrets import load_secrets
from src.aioworxmower.session import MowerSession

async def main():
    sec = load_secrets()
    sess = MowerSession(
        username=sec.get("username",""),
        password=sec.get("password",""),
        client_id=sec.get("client_id",""),
        client_secret=sec.get("client_secret",""),
    )
    await sess.connect()
    dev = sess.get_device()
    print("Connected:", dev.serial, "topic:", dev.topic_status)
    await asyncio.sleep(5)
    await sess.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
