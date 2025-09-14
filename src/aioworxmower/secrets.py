
import os, yaml

def load_secrets(path: str = "secrets.yaml") -> dict:
    data = {}
    if os.getenv("WORX_USER") and os.getenv("WORX_PASS"):
        data["username"] = os.getenv("WORX_USER")
        data["password"] = os.getenv("WORX_PASS")
        data["client_id"] = os.getenv("WORX_CLIENT_ID", "")
        data["client_secret"] = os.getenv("WORX_CLIENT_SECRET", "")
        return data
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    return data
