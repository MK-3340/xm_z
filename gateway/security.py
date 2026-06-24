import json 
import hmac
import hashlib
import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT  / "configs" / "devices.json"
HMAC_SECRET_ENV = "IOT_HMAC_SECRET"


def load_allowed_devices(
        config_path: str | Path = DEFAULT_CONFIG_PATH,
) -> set[str]:
    path = Path(config_path)

    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"device whitlist file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid device whitelist JSON: {path}") from exc
    
    devices = config.get("allowed_devices")

    if not isinstance(devices, list):
        raise ValueError("allowed_devices must be a list.")
    
    if not all(
        isinstance(device_id, str) and device_id for device_id in devices
    ):
        raise ValueError("allowed devices must be contain non-empty strings.")
    
    return set(devices)


def is_allowed_device(
        device_id: str,
        config_path: str | Path = DEFAULT_CONFIG_PATH,
) -> bool:
    return device_id in load_allowed_devices(config_path)
    

def get_hmac_secret() -> str:
    secret = os.getenv(HMAC_SECRET_ENV)

    if not secret:
        raise ValueError(
            f"{HMAC_SECRET_ENV} is not set."
            "Set the same secret in the publisher and gateway terminals."  
            )
    
    return secret


def canonical_payload(data: dict) -> str:
    payload_without_signature = {
        key: value 
        for key,value in data.items() 
        if key != "signature"
    }


    return json.dumps(
        payload_without_signature,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",",":")
    )


def make_signature(
        data: dict,
        secret:str | None = None,
) -> str:
    secret_text = secret if secret is not None else get_hmac_secret()

    return hmac.new(
        secret_text.encode("utf-8"),
        canonical_payload(data).encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def add_signature(
        data: dict,
        secret: str | None = None,
) -> dict:
    signed_data = dict(data)
    signed_data["signature"] = make_signature(signed_data,secret)
    return signed_data


def verify_signature(
        data:dict,
        secret:str | None = None,
) -> bool:
    received_signature = data.get("signature")

    if not isinstance(received_signature,str) or not received_signature:
        return False
    
    expected_signature = make_signature(data,secret)

    return hmac.compare_digest(
        received_signature,
        expected_signature,
    )