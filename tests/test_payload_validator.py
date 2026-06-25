import json
import pytest

from gateway.payload_validator import(
    parse_payload,
    validate_device_data,
    parse_and_validate_payload,
)


def valid_data():
    return {
        "device_id":"motor_001",
        "timestamp":"2026-05-14T10:00:00",
        "nonce":"test-nonce-001",
        "temperature":55.5,
        "vibration":1.2,
        "current":3.4,
        "status":"running",
    }

def test_parse_payload_json():
    payload = json.dumps(valid_data(),ensure_ascii=False)
    data = parse_payload(payload)

    assert data["device_id"] == "motor_001"
    assert data["status"] == "running"


def test_parse_payload_invalid_json():
    payload = "{bad json"

    with pytest.raises(ValueError):
        parse_payload(payload)
    

def test_validate_device_data_success():
    data = valid_data()

    result = validate_device_data(data)

    assert result["device_id"] == "motor_001"


def test_validate_device_data_missing_field():
    data = valid_data()
    del data["temperature"]

    with pytest.raises(ValueError):
        validate_device_data(data)


def test_validate_device_data_temperature_out_of_range():
    data = valid_data()
    data["temperature"] = 150

    with pytest.raises(ValueError):
        validate_device_data(data)

    
def test_parse_and_validate_payload_success():
    payload = json.dumps(valid_data(),ensure_ascii=False)

    data = parse_and_validate_payload(payload)

    assert data["device_id"] == "motor_001"
    assert data["temperature"] == 55.5

def test_validata_device_data_empty_device_id():
    data = valid_data()
    data["device_id"]=""

    with pytest.raises(ValueError):
        validate_device_data(data)

    
def test_validata_device_data_invalid_status():
    data = valid_data()
    data["status"] = "broken"

    with pytest.raises(ValueError):
        validate_device_data(data)


def test_validata_device_data_current_out_of_range():
    data = valid_data()
    data["current"] = 99

    with pytest.raises(ValueError):
        validate_device_data(data)

def test_vaildator_device_data_empty_timestamp():
    data = valid_data()
    data["timestamp"] = ""
    
    with pytest.raises(ValueError):
        validate_device_data(data)


