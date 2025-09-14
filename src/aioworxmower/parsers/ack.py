from __future__ import annotations
from typing import Optional, Dict, Any

def find_ack_id(payload: Dict[str, Any]) -> Optional[str]:
    return payload.get('cid') or (payload.get('ack') or {}).get('cid')

def ack_topic_for(serial: str) -> str:
    return f"{serial}/ack"
