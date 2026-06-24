import json

import pytest

from gateway.security import is_allowed_device


def write_devices_config(tmp_path, devices: list[str]):
    config_path = tmp_path / "devices.json"
    config_path.write_text(
        json.dumps(
            {"allowed_devices": devices},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return config_path


def test_allowed_device_returns_true(tmp_path):
    config_path = write_devices_config(
        tmp_path,
        ["motor_001"],
    )

    result = is_allowed_device(
        "motor_001",
        config_path,
    )

    assert result is True


def test_unknown_device_returns_false(tmp_path):
    config_path = write_devices_config(
        tmp_path,
        ["motor_001"],
    )

    result = is_allowed_device(
        "hacker_001",
        config_path,
    )

    assert result is False


def test_invalid_device_list_raises_error(tmp_path):
    config_path = tmp_path / "devices.json"
    config_path.write_text(
        json.dumps({"allowed_devices": "motor_001"}),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="allowed_devices must be a list",
    ):
        is_allowed_device(
            "motor_001",
            config_path,
        )


def test_default_whitelist_path_does_not_depend_on_working_directory(monkeypatch,tmp_path,):
    monkeypatch.chdir(tmp_path)

    assert is_allowed_device("motor_001") is True
    assert is_allowed_device("hacker_001") is False

    