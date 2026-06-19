import json

from database.db_manager import query_latest_sensor_data


def main():
    latest_data = query_latest_sensor_data(limit=10)

    if not latest_data:
        print("No sensor data found.")
        return 
    
    print(json.dumps(latest_data,ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()