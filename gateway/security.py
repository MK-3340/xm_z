import json 
from pathlib import Path


DEFAULT_CONFIG_PATH = Path("configs/device.json")


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
    allowed_devices = load_allowed_devices(config_path)
    return device_id in allowed_devices
    
