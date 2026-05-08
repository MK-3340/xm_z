from simulators.virtual_device import generate_device_data

def test_generate_data_has_required_fields():
    data = generate_device_data()

    required_fields={
        "device_id",
        "timestamp",
        "temperature",
        "vibration",
        "current",
        "status"
    }
    assert required_fields.issubset(data.keys())
def test_generate_device_data_value_range():
    data = generate_device_data()

    assert data["device_id"] == "motor_001"
    assert 35.0 <= data["temperature"] <=85.0
    assert data["vibration"] <= 3.0
    assert 1.0 <= data["current"] <=10.0
    assert data["status"] == "running"
    
