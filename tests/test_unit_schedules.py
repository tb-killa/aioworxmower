import pytest
from src.aioworxmower.schedules.model import WeekSchedule, DaySchedule
from src.aioworxmower.schedules.worx import to_vendor_payload, from_vendor_payload

pytestmark = pytest.mark.unit

def test_roundtrip_schedule():
    week = WeekSchedule(days=[
        DaySchedule(True, "08:00", 60),
        DaySchedule(False, "00:00", 0),
        DaySchedule(True, "09:30", 45),
        DaySchedule(False, "00:00", 0),
        DaySchedule(True, "07:15", 30),
        DaySchedule(True, "10:00", 90),
        DaySchedule(False, "00:00", 0),
    ])
    js = to_vendor_payload(week)
    rt = from_vendor_payload(js)
    assert len(rt.days) == 7
    assert rt.days[0].enabled is True
    assert rt.days[2].start == "09:30"
    assert rt.days[5].duration_min == 90
