import json

import pytest

from gateway.config import load_runtime_config


def test_load_runtime_config(tmp_path):
    config_path = tmp_path / "config.json"

    config_path.write_text(
        json.dumps(
            {
                "broker_host": "localhost",
                "broker_port": 1883,
                "telemetry_topic": "factory/motor_001/telemetry",
                "db_path": "data/test.db",
            }
        ),
        encoding="utf-8",
    )

    config = load_runtime_config(config_path)

    assert config["broker_host"] == "localhost"
    assert config["broker_port"] == 1883
    assert config["db_path"] == "data/test.db"


def test_load_runtime_config_rejects_invalid_port(tmp_path):
    config_path = tmp_path / "config.json"

    config_path.write_text(
        json.dumps(
            {
                "broker_host": "localhost",
                "broker_port": 0,
                "telemetry_topic": "factory/motor_001/telemetry",
                "db_path": "data/test.db",
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="broker_port"):
        load_runtime_config(config_path)