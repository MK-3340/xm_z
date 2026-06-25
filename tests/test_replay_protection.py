from datetime import datetime,timedelta
from gateway.security import check_nonce_once,check_timestamp_window

def test_current_timestamp_is_allowed():
    now = datetime(2026, 6, 25, 20, 0, 0)

    assert check_timestamp_window("2026-06-25T19:59:30",now=now,) is True


def test_expired_timestamp_is_rejected():
    now = datetime(2026, 6, 25, 20, 0, 0)

    assert check_timestamp_window("2026-06-25T19:58:00",now=now,) is False


def test_future_timestamp_within_five_seconds_is_allowed():
    now = datetime(2026, 6, 25, 20, 0, 0)

    assert check_timestamp_window("2026-06-25T20:00:03",now=now) is True


def test_duplicate_nonce_is_rejected():
    seen_nonces:set[tuple[str,str]] = set()

    assert check_nonce_once("motor_001","nonce-001",seen_nonces) is True
    assert check_nonce_once("motor_001","nonce-001",seen_nonces) is False 



def test_same_nonce_from_different_device_is_allowed():
    seen_nonce:set[tuple[str,str]] = set()

    assert check_nonce_once("motor_001","nonce-001",seen_nonce) is True
    assert check_nonce_once("motor_002","nonce-001",seen_nonce) is True
    