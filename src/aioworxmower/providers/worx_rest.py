from __future__ import annotations
from typing import Dict, Any
from .worx import WorxProvider
from ..schedules.model import WeekSchedule
from ..schedules.worx import to_vendor_payload, from_vendor_payload

class WorxSchedules:
    def __init__(self, provider: WorxProvider) -> None:
        self.p = provider
    async def get(self, serial: str) -> WeekSchedule:
        return WeekSchedule(days=[])
    async def set(self, serial: str, week: WeekSchedule) -> Dict[str, Any]:
        return to_vendor_payload(week)
