import json

from gateway.payload_validator import parse_and_validate_payload
from gateway.security import verify_signature
from simulators import mqtt_publisher

TEST_SECRET = "test-secret"


def test_build_signed_payload_passes_validation_and_hmac(monkeypatch):
    raw_data = {
        "device_id": "motor_001",
        "timestamp": "2026-06-25T14:00:00",
        "temperature": 35.0,
        "vibration": 0.5,
        "current": 2.0,
        "status": "running",
    }

    monkeypatch.setenv("IOT_HMAC_SECRET", TEST_SECRET)
    monkeypatch.setattr(
        mqtt_publisher,
        "generate_device_data",
        lambda: raw_data,
    )

    signed_data = mqtt_publisher.build_signed_payload()

    assert "signature" in signed_data
    assert verify_signature(signed_data,TEST_SECRET) is True

    validated = parse_and_validate_payload(json.dumps(signed_data,ensure_ascii=False))

    assert validated["device_id"] == "motor_001"