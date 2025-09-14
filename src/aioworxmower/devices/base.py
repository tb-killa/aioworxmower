from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Optional, Protocol, runtime_checkable
from ..models import MowerState, MowerInfo
from ..commands import CommandTracker
import orjson

@dataclass
class Capability:
    mowing: bool = True
    party_mode: bool = True
    zones: bool = True
    scheduling: bool = True

@runtime_checkable
class Transport(Protocol):
    async def publish(self, topic: str, payload: bytes, qos: int = 1) -> None: ...
    async def subscribe(self, topic: str, handler, qos: int = 1) -> None: ...

class Device:
    def __init__(self, *, serial: str, transport: Transport, topic_status: str, topic_cmd: str,
                 model: Optional[str] = None, name: Optional[str] = None) -> None:
        self.serial = serial
        self.transport = transport
        self.topic_status = topic_status
        self.topic_cmd = topic_cmd
        self.info = MowerInfo(serial=serial, model=model, name=name)
        self.state = MowerState()
        self.cap = Capability()
        self.cmd = CommandTracker()

    async def handle_status(self, payload: Dict[str, Any]) -> None:
        self.state.raw = payload
        self.state.online = True
        self.state.battery_percent = payload.get("battery", self.state.battery_percent)
        self.state.status_text = payload.get("status", self.state.status_text)

    async def send(self, body: Dict[str, Any], *, wait_ack: bool = False, timeout: float = 10.0):
        cid = self.cmd.new()
        body.setdefault("cid", cid)
        await self.transport.publish(self.topic_cmd, orjson.dumps(body))
        if wait_ack:
            return await self.cmd.wait(cid, timeout=timeout)

    async def start(self) -> None: await self.send({"cmd": 1})
    async def pause(self) -> None: await self.send({"cmd": 4})
    async def stop(self) -> None:  await self.send({"cmd": 2})
    async def home(self) -> None:  await self.send({"cmd": 3})
    async def set_party_mode(self, enabled: bool) -> None:
        await self.send({"cfg": {"partyMode": bool(enabled)}})
