from database.db_manager import insert_sensor_data,query_latest_sensor_data


def make_data(index: int) -> dict:
    return{
        "device_id": "motor_001",
        "timestamp": f"2026-05-25T10:00:{index:02d}",
        "temperature": 50.0 + index,
        "viration": 1.0,
        "current": 3.0,
        "status": "running",
    }

def test_query_latest_sensor_data_returns_recent_10_records(tmp_path):
    db_path = tmp_path / "test_iot_data.db"

    for i in range(12):
        insert_sensor_data(make_data,str(db_path))

        rows = query_latest_sensor_data(limit=10,db_path=str(db_path))

        assert len(rows) == 10
        assert rows[0]["timestamp"] == "2026-05-25T10:00:11"
        assert rows[-1]["timestamp"] == "2026-05-25T10:00:02"


def test_query_latest_sensor_data_empty_db_return_enpry_list(tmp_path):
    db_path = tmp_path / "empty_iot_data.db"

    rows = query_latest_sensor_data(limit=10,db_path=str(db_path))

    assert rows == []