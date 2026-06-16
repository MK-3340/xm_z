from anomaly_detection.zscore_detector import (
    calculate_zscore,
    detect_zsore_anomaly,
)


def make_data() -> dict:
    return {
        "device_id": "motor_001",
        "timestamp": "2026-05-25T10:00:00",
        "temperature": 40.0,
        "vibration": 1.0,
        "current": 3.0,
        "status": "running",
    }


def test_calculate_zscore_normal_value():
    zscore = calculate_zscore(40.0, [39.0, 40.0, 41.0])

    assert abs(zscore) < 3


def test_calculate_zscore_far_value():
    zscore = calculate_zscore(100.0, [39.0, 40.0, 41.0, 40.5, 39.5])

    assert abs(zscore) >= 3


def test_calculate_zscore_empty_history_should_return_zero():
    zscore = calculate_zscore(100.0, [])

    assert zscore == 0.0


def test_calculate_zscore_std_zero_should_return_zero():
    zscore = calculate_zscore(100.0, [40.0, 40.0, 40.0])

    assert zscore == 0.0


def test_detect_zsore_normal_temperature_should_not_alarm():
    data = make_data()
    history_values = [39.0, 40.0, 41.0, 40.5, 39.5]

    result = detect_zsore_anomaly(
        data=data,
        history_value=history_values,
        field="temperature",
    )

    assert result["is_anomaly"] is False
    assert result["alarm_type"] is None
    assert result["alarm_reason"] is None
    assert result["severity"] == "normal"


def test_detect_zsore_high_temperature_should_alarm():
    data = make_data()
    data["temperature"] = 100.0
    history_values = [39.0, 40.0, 41.0, 40.5, 39.5]

    result = detect_zsore_anomaly(
        data=data,
        history_value=history_values,
        field="temperature",
    )

    assert result["is_anomaly"] is True
    assert result["alarm_type"] == "zscore"
    assert "temperature" in result["alarm_reason"]
    assert result["severity"] == "medium"


def test_detect_zsore_high_vibration_should_alarm():
    data = make_data()
    data["vibration"] = 8.0
    history_values = [0.8, 1.0, 1.1, 0.9, 1.2]

    result = detect_zsore_anomaly(
        data=data,
        history_value=history_values,
        field="vibration",
    )

    assert result["is_anomaly"] is True
    assert result["alarm_type"] == "zscore"
    assert "vibration" in result["alarm_reason"]


def test_detect_zsore_high_current_should_alarm():
    data = make_data()
    data["current"] = 25.0
    history_values = [2.8, 3.0, 3.1, 2.9, 3.2]

    result = detect_zsore_anomaly(
        data=data,
        history_value=history_values,
        field="current",
    )

    assert result["is_anomaly"] is True
    assert result["alarm_type"] == "zscore"
    assert "current" in result["alarm_reason"]


def test_detect_zsore_std_zero_should_not_crash():
    data = make_data()
    data["temperature"] = 100.0
    history_values = [40.0, 40.0, 40.0]

    result = detect_zsore_anomaly(
        data=data,
        history_value=history_values,
        field="temperature",
    )

    assert result["is_anomaly"] is False
    assert result["severity"] == "normal"
    assert result["zscore"] == 0.0