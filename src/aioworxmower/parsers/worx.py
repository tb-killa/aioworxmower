from __future__ import annotations
from typing import Dict, Any
from ..codes.status_codes import STATUS_TEXT
from ..codes.error_codes import ERROR_TEXT

def parse_status(payload: Dict[str, Any]) -> Dict[str, Any]:
    res: Dict[str, Any] = {}
    for key in ("battery", "batteryLevel", "batt_pct", "bt"):
        if key in payload:
            res["battery"] = payload[key]
            break
    status_text = payload.get("status") or payload.get("state") or payload.get("statusText")
    if status_text is None:
        code = payload.get("st") or payload.get("stateCode")
        if isinstance(code, int):
            status_text = STATUS_TEXT.get(code, f"code_{code}")
    res["status_text"] = status_text
    if "error" in payload and isinstance(payload["error"], dict):
        res["error_text"] = payload["error"].get("message")
    else:
        err = payload.get("error") or payload.get("errorCode")
        if isinstance(err, int):
            res["error_text"] = ERROR_TEXT.get(err, f"code_{err}")
        else:
            res["error_text"] = payload.get("errorText")
    gps = payload.get("gps") or {}
    res["latitude"] = gps.get("lat") or payload.get("latitude")
    res["longitude"] = gps.get("lon") or payload.get("longitude")
    res["zone"] = payload.get("zone") or payload.get("currentZone")
    return res

_CMD = {"start": 1, "stop": 2, "home": 3, "pause": 4}

def build_command(kind: str, extra: Dict[str, Any] | None = None) -> Dict[str, Any]:
    body: Dict[str, Any] = {}
    if kind in _CMD:
        body = {"cmd": _CMD[kind]}
    elif kind == "party_mode":
        body = {"cfg": {"partyMode": bool((extra or {}).get("enabled", False))}}
    else:
        body = {"cmd": kind}
    if extra:
        body.update(extra)
    return body
