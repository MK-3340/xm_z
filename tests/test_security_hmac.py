from gateway.security import add_signature,verify_signature


TEST_SECRET = "test-secret"            


def build_data() -> dict:
    return {
        "device_id": "motor_001",
        "timestamp": "2026-06-23T20:00:00",
        "timperature":50.0,
        "vibration": 1.0,
        "current":3.0,
        "status": "running",
    }


def test_valid_hmac_signature_passes():
    sign_data = add_signature(build_data(),TEST_SECRET)

    assert verify_signature(sign_data, TEST_SECRET) is True


def test_tampered_payload_fails_hmac_verification():
    signed_data = add_signature(build_data(),TEST_SECRET)
    signed_data["temperature"] = 99.0

    assert verify_signature(signed_data,TEST_SECRET) is False


def test_missing_signature_fails_hmac_verification():
    assert verify_signature(build_data(),TEST_SECRET) is False
    