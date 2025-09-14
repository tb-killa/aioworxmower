from __future__ import annotations
from typing import Dict, Any, Optional
from .base import Device
from ..parsers.worx import parse_status, build_command
from ..parsers.ack import find_ack_id

class WorxDevice(Device):
    def __init__(self, *, serial: str, transport, region: str="eu", model: Optional[str]=None, name: Optional[str]=None):
        topic_status = f"worx/{serial}/status"
        topic_cmd    = f"worx/{serial}/command"
        super().__init__(serial=serial, transport=transport, topic_status=topic_status, topic_cmd=topic_cmd,
                         model=model, name=name)

    async def handle_status(self, payload: Dict[str, Any]) -> None:
        m = parse_status(payload)
        self.state.online = True
        self.state.battery_percent = m.get("battery")
        self.state.status_text = m.get("status_text")
        self.state.error_text = m.get("error_text")
        self.state.latitude = m.get("latitude")
        self.state.longitude = m.get("longitude")
        self.state.zone = m.get("zone")
        self.state.raw = payload
        cid = find_ack_id(payload) if isinstance(payload, dict) else None
        if cid:
            self.cmd.resolve(cid, payload)

    async def start(self) -> None: await self.send(build_command("start"))
    async def pause(self) -> None: await self.send(build_command("pause"))
    async def stop(self)  -> None: await self.send(build_command("stop"))
    async def home(self)  -> None: await self.send(build_command("home"))
    async def set_party_mode(self, enabled: bool) -> None:
        await self.send(build_command("party_mode", {"enabled": bool(enabled)}))
