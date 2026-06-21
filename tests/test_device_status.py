from datetime import datetime, timedelta
from pathlib import Path
from database.db_manager import insert_sensor_data, query_device_status


def build_data(timestamp: str) -> dict:
    return {
        "device_id": "motor_001",
        "timestamp": timestamp,
        "temperature":55.5,
        "vibration":1.2,
        "current":3.4,
        "status":"running",
    }


def test_query_device_status_returns_none_when_no_data(tmp_path: Path):
    db_path = tmp_path / "test_iot_data.db"

    result = query_device_status("motor_001", str(db_path))

    assert result is None


def test_device_is_online_when_last_seen_is_recent(tmp_path: Path):
    db_path = tmp_path / "test_iot_data.db"
    now = datetime(2026, 6, 21, 12, 0, 0)

    insert_sensor_data(build_data((now - timedelta(seconds=2)).isoformat()),str(db_path))

    result = query_device_status(
        "motor_001",
        str(db_path),
        online_seconds=5,
        now=now,
    )

    assert result is not None
    assert result["online_status"] == "online"
    assert result["device_status"] == "running"


def test_device_is_offline_when_last_seen_id_too_old(tmp_path: Path):
    db_path = tmp_path / "test_iot_data.db"
    now = datetime(2026,6, 21, 12, 0, 0)

    insert_sensor_data(build_data((now - timedelta(seconds=8)).isoformat()),str(db_path),)

    result = query_device_status(
        "motor_001",
        str(db_path),
        online_seconds=5,
        now=now,
    )

    assert result is not None
    assert result["online_status"] == "offline"                  