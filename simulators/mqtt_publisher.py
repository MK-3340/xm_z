import json
import time

import paho.mqtt.client as mqtt  # type: ignore

from simulators.virtual_device import generate_device_data

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "factory/motor_001/telemetry"

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(BROKER_HOST,BROKER_PORT,60)

    print(f"MQTT publisher started. topic={TOPIC}")

    while True:
        data = generate_device_data()
        payload = json.dumps(data,ensure_ascii=False)

        client.publish(TOPIC,payload)
        print(payload)

        time.sleep(1)

if __name__ == "__main__":
    main()

