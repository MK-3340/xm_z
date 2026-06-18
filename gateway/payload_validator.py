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
        raise ValueError(f"Missing required fields：{sorted(missing_fields)}")
    
    if not isinstance(data["device_id"],str) or not data["device_id"]:
        raise ValueError("device_id must be a non-empy string.")
    
    if not isinstance(data["timestamp"], str) or not data["timestamp"]:
        raise ValueError("timestamp must be a non-emty string.")
    
    temperature = data["temperature"]
    vibration = data["vibration"]
    current = data["current"]

    if not isinstance(temperature,(int,float)):
        raise ValueError("temperature must be a number.")
    
    if not isinstance(vibration,(int,float)):
        raise ValueError("vibration must be a number.")
    
    if not isinstance(current,(int,float)):
        raise ValueError("current must be a munber.")
    
    if not 0 <= temperature <= 120:
        raise ValueError("temperature out of range.")
    
    if not 0 <= vibration <= 10:
        raise ValueError("vibration out of range.")
    
    if not 0<= current <=30:
        raise ValueError("current out of range.")
    
    if data["status"] not in {"running","warning","alarm","offline"}:
        raise ValueError("invalid status value.")
    
    return data


def parse_and_validate_payload(payload:str)->dict:
    data = parse_payload(payload)
    return validate_device_data(data)