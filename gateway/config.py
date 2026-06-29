import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent 
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "config.json"


def load_runtime_config(config_path:str | Path = DEFAULT_CONFIG_PATH) -> dict:
    path = Path(config_path)

    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"config file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid config JSON: {path}") from exc
    
    required_keys = [
        "broker_host",
        "broker_port",
        "telemetry_topic",
        "db_path",
    ]

    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        raise ValueError(f"missing config keys:{missing_keys}")
    
    if not isinstance(config["broker_host"],str) or not config["broker_host"]:
        raise ValueError("broker_host must be a non-empty string")
    
    if (
        not isinstance(config["broker_port"],int)
        or not 1 <= config["broker_port"] <=65535   
    ):
        raise ValueError("broker_port must be between 1 and 65535")
    
    if not isinstance(config["telemetry_topic"],str) or not config["telemetry_topic"]:
        raise ValueError("telemetry_tpoic must be a non-emtry string")
    
    if not isinstance(config["db_path"],str) or not config["db_path"]:
        raise ValueError("db_path must be a non-emtry string")
    
    return config