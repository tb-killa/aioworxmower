from __future__ import annotations
import asyncio, uuid
from typing import Dict, Any

class CommandTracker:
    def __init__(self) -> None:
        self._futs: Dict[str, asyncio.Future] = {}

    def new(self) -> str:
        cid = uuid.uuid4().hex[:12]
        loop = asyncio.get_event_loop()
        self._futs[cid] = loop.create_future()
        return cid

    def resolve(self, cid: str, payload: Any) -> None:
        fut = self._futs.pop(cid, None)
        if fut and not fut.done():
            fut.set_result(payload)

    async def wait(self, cid: str, timeout: float = 10.0) -> Any:
        fut = self._futs.get(cid)
        if not fut:
            raise RuntimeError("unknown command id")
        return await asyncio.wait_for(fut, timeout=timeout)
