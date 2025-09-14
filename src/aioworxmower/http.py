from __future__ import annotations
from typing import Any, Dict, Optional
import anyio, httpx
from .logging import get_logger
import orjson

class HttpClient:
    def __init__(self, base_url: str, timeout: float = 15.0, debug: bool = False) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._token: Optional[str] = None
        self.debug = debug
        self.log = get_logger("http")

    def set_token(self, token: Optional[str]) -> None:
        self._token = token

    async def request(self, method: str, path: str, *, json: Any | None = None, data: Any | None = None, headers: Dict[str, str] | None = None) -> httpx.Response:
        url = path if path.startswith("http") else f"{self.base_url}{path if path.startswith('/') else '/'+path}"
        h = dict(headers or {})
        if self._token:
            h["Authorization"] = f"Bearer {self._token}"
        if self.debug:
            self.log.debug("HTTP %s %s json=%s data=%s", method, url, bool(json), bool(data))
        async with httpx.AsyncClient(timeout=self.timeout) as s:
            delay = 0.2
            for attempt in range(4):
                try:
                    r = await s.request(method, url, json=json, data=data, headers=h)
                    if self.debug:
                        self.log.debug("HTTP %s -> %s", url, r.status_code)
                    if r.status_code in (429, 500, 502, 503, 504):
                        raise httpx.HTTPStatusError("retryable", request=r.request, response=r)
                    return r
                except (httpx.TransportError, httpx.HTTPStatusError):
                    if attempt == 3:
                        raise
                    await anyio.sleep(delay)
                    delay *= 2
