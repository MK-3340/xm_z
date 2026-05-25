import sqlite3
from pathlib import Path


def init_db(db_path:str = "data/iot_data.db") -> None:
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True,exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor

    cursor.excute(
        """
        CREATE TABLE IF NOT EXISTS sensor_data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        temperature REAL NOT NULL,
        vibration REAL NOT NULL,
        current REAL NOT NULL,
        status TEXT NOT NULL 
        )
        """
    )

def insert_sensor_data(db_path,data):
def get_latest_sensor_data(db_path):