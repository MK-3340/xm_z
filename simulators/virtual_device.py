import json
import random
import time
from datetime import datetime

def generate_device_data(device_id="motor_001"):
        data ={
        "device_id":device_id,
        "timestamp":datetime.now().isoformat(timespec="seconds"),
        "temperature":round(random.uniform(35.0,85.0),2),
        "vibration":round(random.uniform(0.1,3.0),2),
        "current":round(random.uniform(1.0,10.0),2),
        "status":"running"
        }
        return data

def main():
    while True:
        data = generate_device_data()
        json_data=json.dumps(data,ensure_ascii=False)
        print(json_data)
        time.sleep(1)

if __name__=="__main__":
        main()