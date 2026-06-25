import paho.mqtt.client as mqtt # type: ignore
from gateway.payload_validator import parse_and_validate_payload
from database.db_manager import insert_sensor_data,insert_alarm
from anomaly_detection.threshold_detector import detect_threshold_anomaly
from gateway.security import is_allowed_device, verify_signature,check_nonce_once,check_timestamp_window

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
        data = parse_and_validate_payload(payload)
        if not is_allowed_device(data["device_id"]):
            raise ValueError(f"device_id is not allowed:{data['device_id']}")
        
        if not verify_signature(data):
            raise ValueError("invalid HMAC signature")
        
        if not check_timestamp_window(data["timestamp"]):
            raise ValueError("timestamp is expired or invalid")
        
        if not check_nonce_once(data["device_id"],data["nonce"]):
            raise ValueError("duplicate nonce detected")

        insert_sensor_data(data)

        result = detect_threshold_anomaly(data)
        
        if result["is_anomaly"]:
            alarm = {
                "device_id":data["device_id"],
                "timestamp":data["timestamp"],
                "alarm_type":result["alarm_type"],
                "alarm_reason":result["alarm_reason"],
                "severity":result["severity"],
            }
            insert_alarm(alarm)
            print(f"[ALARM SAVED]{alarm}")



    except ValueError as e:
        print(f"[INVALID MESSAGE] topic={msg.topic},error={e},payload={payload}")
        return
    print(
        "[VALID DATA] "
        f"device_id={data['device_id']},"
        f"timestamp={data['timestamp']},"
        f"temperature={data['temperature']},"
        f"vibration={data['vibration']},"
        f"current={data['current']},"
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