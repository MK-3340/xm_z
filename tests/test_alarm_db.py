import sqlite3

from database.db_manager import init_db, insert_alarm


def make_data() -> dict:
    return{
        "device_id": "motor_001",
        "timestamp": "2026-05-25T10:00:00",
        "alarm_type": "threshold",
        "alarm_reason": "temperature too hign: 100",
        "severity": "high",
    }


def test_insert_alarm(tmp_path):
    db_path = tmp_path / "test_iot_data.db"

    init_db(str(db_path))
    insert_alarm(make_data(),str(db_path))

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT device_id,timestamp,alarm_type,alarm_reason,severity
        FROM alarms
        ORDER BY id DESC
        LIMIT 1
        """
    )
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row[0] == "motor_001"
    assert row[2] == "threshold"
    assert "temperature" in row[3]
    assert row[4] == "high"

def test_insert_alarm_should_save_to_alarms_table(tmp_path):
    db_path = tmp_path / "test_iot_data.db"

    init_db(str(db_path))

    alarm = {
        "device_id": "motor_001",
        "timestamp": "2026-05-25T10:00:00",
        "alarm_type": "threshold",
        "alarm_reason": "temperature too high: 100",
        "severity": "high",
    }

    insert_alarm(alarm,str(db_path))

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT device_id,timestamp,alarm_type,alarm_reason,severity
        FROM alarms
        """
    )
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row[0] == "motor_001"
    assert row[1] == "2026-05-25T10:00:00"
    assert row[2] == "threshold"
    assert "temperature" in row[3]
    assert row[4] == "high"
