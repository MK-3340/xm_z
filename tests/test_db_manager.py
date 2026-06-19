from database.db_manager import (
    init_db,
    insert_sensor_data,
    get_latest_sensor_data,
)


def valid_data():
    return {
        "device_id": "motor_001",
        "timestamp": "2026-05-25T10:00:00",
        "temperature": 55.5,
        "vibration": 1.2,
        "current": 3.4,
        "status": "running",
    }


def test_init_db_creates_database_file(tmp_path):
    db_path = tmp_path / "test_iot_data.db"

    init_db(str(db_path))

    assert db_path.exists()


def test_insert_and_get_latest_sensor_data(tmp_path):
    db_path = tmp_path / "test_iot_data.db"

    init_db(str(db_path))

    assert db_path.exists()


def test_insert_and_get_latest_sensor_data(tmp_path):
    db_path =tmp_path / "test_iot_data.db"
    data = valid_data()

    insert_sensor_data(data, str(db_path))
    latest = get_latest_sensor_data(str(db_path))

    assert latest is not None
    assert latest["device_id"] == "motor_001"
    assert latest["temperature"] == 55.5
    assert latest["vibration"] == 1.2
    assert latest["current"] == 3.4
    assert latest["status"] == "running"


