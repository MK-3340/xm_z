import json

from database.db_manager import get_latest_sensor_data


def main():
    latest = get_latest_sensor_data()

    if latest is None:
        print("No sensor data found.")
        return 
    
    print(json.dumps(latest,ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()