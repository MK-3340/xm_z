import json
import time

import paho.mqtt.client as mqtt  # type: ignore

from gateway.security import add_signature
from simulators.virtual_device import generate_device_data

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "factory/motor_001/telemetry"


def build_signed_payload() -> dict:
    data = generate_device_data()
    return add_signature(data)


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(BROKER_HOST,BROKER_PORT,60)

    print(f"MQTT publisher started. topic={TOPIC}")

    while True:
        data = build_signed_payload()
        payload = json.dumps(data,ensure_ascii=False)

        client.publish(TOPIC,payload)
        print(payload)

        time.sleep(1)

if __name__ == "__main__":
    main()

