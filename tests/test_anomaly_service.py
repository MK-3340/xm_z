from anomaly_detection.anomaly_service import analyze_sensor_data


def make_data() -> dict:
    return {
        "device_id": "motor_001",
        "timestamp": "2026-05-25T10:00:00",
        "temperature": 40.0,
        "vibration": 1.0,
        "current": 3.0,
        "status": "running",
    }


def test_analyze_normal_data_should_not_alarm():
    data = make_data()

    history = {
        "temperature": [39.0,40.0,41.0],
        "vibration": [0.8,1.0,1.1],
        "current": [2.8,3.0,3.1],
    }

    result = analyze_sensor_data(data,history)

    assert result["is_anomaly"] is False
    assert result["alarm_type"] is None
    assert result["severity"] == "normal"


def test_threshold_anomaly_should_return_threshold_first():
    data = make_data()
    data["temperature"] = 100.0

    history = {
        "temperature": [39.0,40.0,41.0],
        "vibration": [0.8,1.0,1.1],
        "current": [2.8,3.0,3.1],
    }

    result = analyze_sensor_data(data,history)

    assert result["is_anomaly"] is True
    assert result["alarm_type"] is "threshold"
    assert "temperature" in result["alarm_reason"]
    assert result["severity"] == "high"


def test_analyze_zscore_anomaly_should_return_zscore_when_threshold_normal():
    data = make_data() 
    data["temperature"] = 80.0

    history = {
        "temperature": [39.0,40.0,41.0,40.5,39.5],
        "vibration": [0.8,1.0,1.1],
        "current":[2.8,3.0,3.1],
    }

    result = analyze_sensor_data(data,history)

    assert result["is_anomaly"] is True
    assert result["alarm_type"] == "zscore"
    assert "temperature" in result["alarm_reason"]
    assert result["severity"] == "medium"


def test_analyze_without_history_should_not_crash():
    data = make_data()

    result = analyze_sensor_data(data)

    assert result["is_anomaly"] is False
    assert result["severity"] == "normal"


def test_zscore_anomaly_should_be_detected():
    data = make_data()
    data["vibration"] = 8.0

    history = {
        "temperature": [54, 55, 56, 55],
        "vibration": [1.0, 1.1, 1.2, 1.1, 1.0],
        "current": [3.0, 3.2, 3.1, 3.3],
    }

    result = analyze_sensor_data(data, history)

    assert result["is_anomaly"] is True
    assert result["alarm_type"] in {"threshold","zscore"}    