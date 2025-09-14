"""Overview: Worx Landroid Cloud provider."""
from __future__ import annotations
from typing import List, Optional, Dict
import os
from .base import VendorProvider, VendorDeviceMeta, Bootstrap
from ..http import HttpClient

WORX_API_BASE = os.getenv("WORX_API_BASE", "https://api.worxlandroid.com")
OAUTH_PATH = os.getenv("WORX_OAUTH_PATH", "/api/v2/oauth/token")
DEVICES_PATH = os.getenv("WORX_DEVICES_PATH", "/api/v2/product-items")
USERDATA_PATH = os.getenv("WORX_USERDATA_PATH", "/api/v2/user-data")

class WorxProvider(VendorProvider):
    def __init__(self, *, username: str, password: str, client_id: str | None = None, client_secret: str | None = None, base_url: str | None = None) -> None:
        self.username = username
        self.password = password
        self.client_id = client_id or os.getenv("WORX_CLIENT_ID", "")
        self.client_secret = client_secret or os.getenv("WORX_CLIENT_SECRET", "")
        self.api = HttpClient(base_url or WORX_API_BASE)
        self._access_token: Optional[str] = None

    async def login(self) -> None:
        data = {
            "username": self.username,
            "password": self.password,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "password",
        }
        r = await self.api.request("POST", OAUTH_PATH, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        r.raise_for_status()
        js = r.json()
        token = js.get("access_token")
        if not token:
            raise RuntimeError("No access_token in Worx response")
        self._access_token = token
        self.api.set_token(token)

    async def list_devices(self) -> List[VendorDeviceMeta]:
        r = await self.api.request("GET", DEVICES_PATH)
        r.raise_for_status()
        out = []
        for item in (r.json() or []):
            serial = str(item.get("serial_number") or item.get("serial") or item.get("id"))
            name = item.get("name") or item.get("product_name")
            model = item.get("model") or item.get("product")
            topics = {"status": f"{serial}/status", "command": f"{serial}/command"}
            out.append(VendorDeviceMeta(serial=serial, name=name, model=model, topics=topics))
        return out

    async def get_bootstrap(self) -> Bootstrap:
        r = await self.api.request("GET", USERDATA_PATH)
        r.raise_for_status()
        js = r.json() or {}
        endpoint = js.get("aws_iot_endpoint") or js.get("mqtt_endpoint") or "iot.example"
        client_id = js.get("client_id") or js.get("mqtt_client_id") or "unknown-client"
        headers = js.get("websocket_headers") or {}
        return Bootstrap(endpoint=endpoint, client_id=client_id, websocket=True, headers=headers)
