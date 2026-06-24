import json
from types import SimpleNamespace

import gateway.mqtt_subscriber as mqtt_subscriber


def build_data() -> dict:
    return {
        "device_id": "motor_001",
        "timestamp": "2026-06-23T20:00:00",
        "temperature": 50.0,
        "vibration": 1.0,
        "current": 3.0,
        "status": "running",
        "signature": "fake-signature",
    }


def test_valid_message_is_persisted_once(monkeypatch):
    data = build_data()
    inserted_sensor_data = []
    inserted_alarms = []

    monkeypatch.setattr(
        mqtt_subscriber,
        "parse_and_validate_payload",
        lambda payload: data,
    )

    monkeypatch.setattr(
        mqtt_subscriber,
        "is_allowed_device",
        lambda device_id: True,
    )

    monkeypatch.setattr(
        mqtt_subscriber,
        "verify_signature",
        lambda payload: True,
    )

    monkeypatch.setattr(
        mqtt_subscriber,
        "insert_sensor_data",
        lambda payload: inserted_sensor_data.append(payload),
    )

    monkeypatch.setattr(
        mqtt_subscriber,
        "detect_threshold_anomaly",
        lambda payload: {
            "is_anomaly": False,
            "alarm_type": None,
            "alarm_reason": None,
            "severity": "normal",
        },
    )

    monkeypatch.setattr(
        mqtt_subscriber,
        "insert_alarm",
        lambda alarm: inserted_alarms.append(alarm),
    )

    message = SimpleNamespace(
        topic="factory/motor_001/telemetry",
        payload=json.dumps(data).encode("utf-8"),
    )

    mqtt_subscriber.on_message(None, None, message)

    assert inserted_sensor_data == [data]
    assert inserted_alarms == []