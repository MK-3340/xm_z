import json


REQUIRED_FIELDS = {
    "device_id",
    "timestamp",
    "temperature",
    "vibration",
    "current",
    "status"
}


def parse_payload(payload:str)->dict:
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON payload：{e}") from e
    
    if not isinstance(data,dict):
        raise ValueError("Payload must be a JOSN object.")

    return data 


def validate_device_data(data:dict) -> dict:
    missing_fields = REQUIRED_FIELDS - set(data.keys())
    if missing_fields:
        raise
