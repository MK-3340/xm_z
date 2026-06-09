from anomaly_detection.threshold_detector import detect_threshold_anomaly


def make_data() -> dict:
    return {
        "device_id":"motor_001",
        "timestamp":"2026-05-25T10:00:00",
        "temperature":55.5,
        "vibration":1.2,
        "current":3.4,
        "status":"running",
    }


def test_normal_data_should_not_alarm():
    data = make_data()

    result = detect_threshold_anomaly(data)

    assert result["is_anomaly"] is False
    assert result["severity"] == "normal"
    assert result["alarm_reason"] is None


def test_high_temperature_should_alarm():
    data = make_data()
    data["temperature"] = 100

    result = detect_threshold_anomaly(data)

    assert result["is_anomaly"] is True
    assert result["severity"] == "high"
    assert "temperature" in result["alarm_reason"]


def test_high_vibration_should_alarm():
    data = make_data()
    data["vibration"] = 8

    result = detect_threshold_anomaly(data)

    assert result["is_anomaly"] is True
    assert result["severity"] == "high"
    assert "vibration" in result["alarm_reason"]


def test_high_current_should_alarm():
    data = make_data()
    data["current"] = 25

    result = detect_threshold_anomaly(data)

    assert result["is_anomaly"] is True
    assert result["severity"] == "high"
    assert "current" in result["alarm_reason"]




