from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class MowerInfo:
    serial: str
    model: Optional[str] = None
    name: Optional[str] = None

@dataclass
class MowerState:
    online: bool = False
    battery_percent: Optional[int] = None
    status_text: Optional[str] = None
    error_text: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    zone: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)
