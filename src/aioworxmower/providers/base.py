from __future__ import annotations
from typing import Protocol, List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class VendorDeviceMeta:
    serial: str
    model: Optional[str] = None
    name: Optional[str] = None
    topics: Dict[str, str] | None = None

@dataclass
class Bootstrap:
    endpoint: str
    client_id: str
    websocket: bool = True
    headers: Dict[str, str] | None = None
    cert_pem: Optional[str] = None
    key_pem: Optional[str] = None

class VendorProvider(Protocol):
    async def login(self) -> None: ...
    async def list_devices(self) -> List[VendorDeviceMeta]: ...
    async def get_bootstrap(self) -> Bootstrap: ...
