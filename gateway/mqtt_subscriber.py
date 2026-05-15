import paho.mqtt.client as mqtt # type: ignore
from gateway.payload_validator import parse_and_validata_payload

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "factory/motor_001/telemetry"

def on_connect(client, userdata, flags, reason_code, properties):
    print("MQTT subscriber connected.")
    client.subscribe(TOPIC)
    print(f"Subscribed topic: {TOPIC}")


def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    
    try:
        data = parse_and_validata_payload(payload)
    except:ValueError as e:
        print(f"{INVALID MESSAGE} topic={msg.topic},error={e},payload={payload}")
        return
    print(
        "[VALID DATA] "
        f"device_id={data['device_id']},"
        f"timestamp={data['timestemp']},"
        f"temperature={data['temperature']},"
        f"vibration={data['vibration']},"
        f"cerrent={data['cerrent']},"
        f"status={data['status']}"
    )



def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_HOST, BROKER_PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()