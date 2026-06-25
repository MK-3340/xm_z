import json
import time 
import secrets

from datetime import datetime
from gateway.security import add_signature
import paho.mqtt.client as mqtt # type: ignore


BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "factory/motor_001/telemetry"


def make_abnormal_payload(case_name: str) -> dict:
    data = {
        "device_id": "motor_001",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "nonce": secrets.token_hex(16),
        "temperature": 40.0,
        "vibration": 1.0,
        "current": 3.0,
        "status": "running",
    }   
    if case_name == "temperature":
        data["temperature"] = 100.0
        data["status"] = "alarm"
    elif case_name == "vibration":
        data["vibration"] = 8.0 
        data["status"] = "alarm"
    elif case_name == "current":
        data["current"] = 25.0 
        data["status"] = "alarm"
    else:
        raise ValueError(f"unknown abnormal case name: {case_name}")

    return data


def main() -> None:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(BROKER_HOST,BROKER_PORT,60)
    client.loop_start()

    cases = ["temperature","vibration","current"]

    for case_name in cases:
        data = add_signature(make_abnormal_payload(case_name))
        payload = json.dumps(data, ensure_ascii=False)

        info = client.publish(TOPIC,payload)
        info.wait_for_publish()

        print(f"[ABNORMAL PUBLISHED] case={case_name},payload={payload}")
        time.sleep(1)

    client.loop_stop()
    client.disconnect()


if __name__ == "__main__":
    main()