from __future__ import annotations
import asyncio
from typing import Callable, Awaitable, Dict, Any

Handler = Callable[[Dict[str, Any]], Awaitable[None] | None]

class EventBus:
    def __init__(self) -> None:
        self._handlers: Dict[str, list[Handler]] = {}

    def on(self, event: str, handler: Handler) -> None:
        self._handlers.setdefault(event, []).append(handler)

    async def emit(self, event: str, data: Dict[str, Any]) -> None:
        for h in self._handlers.get(event, []):
            res = h(data)
            if asyncio.iscoroutine(res):
                await res
