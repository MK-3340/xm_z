import sqlite3
from pathlib import Path
from datetime import datetime


def init_db(db_path:str = "data/iot_data.db") -> None:
    """
    初始化 SQLite 数据库。
    如果 data 目录不存在，就自动创建。
    如果 sensor_data 表不存在，就自动建表。
    """
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True,exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
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

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS alarms(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            alarm_type TEXT NOT NULL,
            alarm_reason TEXT NOT NULL,
            severity TEXT NOT NULL
        )
        """
    )


    conn.commit()
    conn.close()


def insert_sensor_data(data:dict,db_path: str = "data/iot_data.db")->None:
    '''
    插入一条已经通过的 payload_validator 校验的数据.
    '''
    init_db(db_path)


    conn = sqlite3.connect(db_path)
    cursor =  conn.cursor()

    cursor.execute(
        """
        INSERT INTO sensor_data (
        device_id,
        timestamp,
        temperature,
        vibration,
        current,
        status
        )VALUES(?,?,?,?,?,?)
        """,
        (
            data["device_id"],
            data["timestamp"],
            data["temperature"],
            data["vibration"],
            data["current"],
            data["status"],
        ),
    )

    conn.commit()
    conn.close()

def get_latest_sensor_data(db_path: str = "data/iot_data.db") -> dict|None:
    """
    查询最新一条设备数据。
    没有数据时返回 None。
    """  
    init_db(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            device_id,
            timestamp,
            temperature,
            vibration,
            current,
            status
        FROM sensor_data
        ORDER BY id DESC
        LIMIT 1
        """
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None
    
    return {
        "id": row[0],
        "device_id": row[1],
        "timestamp": row[2],
        "temperature": row[3],
        "vibration": row[4],
        "current": row[5],
        "status": row[6],
    }


def query_latest_sensor_data(
        limit: int = 10,
        db_path: str = "data/iot_data.db"
) -> list[dict]:
    """
    查询最近 N 条传感器数据。
    默认查询最近 10 条。
    """
    if limit <=0:
        raise ValueError("limit must be greather than 0")
    
    init_db(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 
            id,
            device_id,
            timestamp,
            temperature,
            vibration,
            current,
            status
        FROM sensor_data
        ORDER BY timestamp DESC,id DESC
        LIMIT ?
        """,
        (limit,),
    )

    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append(
            {
                "id":row[0],
                "device_id":row[1],
                "timestamp":row[2],
                "temperature":row[3],
                "vibration":row[4],
                "current":row[5],
                "status":row[6],
            }
        )

    return result


def insert_alarm(alarm: dict,db_path: str = "data/iot_data.db") -> None:
    """
    插入一条报警的记录
    alarm 来自 threshld_detector.detect_threshold_anomaly(data)的结果 
    """
    init_db(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO alarms (
        device_id,
        timestamp,
        alarm_type,
        alarm_reason,
        severity
        ) VALUES(?, ?, ?, ?, ?)
        """,
        (
            alarm["device_id"],
            alarm["timestamp"],
            alarm["alarm_type"],
            alarm["alarm_reason"],
            alarm["severity"],
        ),
    )

    conn.commit()
    conn.close()

def query_latest_alarms(
        limit: int = 10,
        db_path: str = "data/iot_data.db"
) -> list[dict]:
    """
    查询最近 N 条报警记录。
    默认查询最近 10 条
    """
    if limit <= 0:
        raise ValueError("limit must be greater than 0")
    
    init_db(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 
            id,
            device_id,
            timestamp,
            alarm_type,
            alarm_reason,
            severity
            FROM alarms
            ORDER BY timestamp DESC, id DESC
            LIMIT ?
        """,
        (limit,),
    )

    rows = cursor.fetchall()
    conn.close()

    result = []

    for row in rows:
        result.append(
            {
                "id":row[0],
                "device_id":row[1],
                "timestamp":row[2],
                "alarm_type":row[3],
                "alarm_reason":row[4],
                "severity":row[5],
            }
        )
    
    return result


def query_device_status(
        device_id: str,
        db_path: str = "data/iot_data.db",
        online_seconds: int = 5,
        now: datetime |None = None,
) -> dict | None:
    """根据最后一次上报的时间判断设备在线状态。"""
    if online_seconds <= 0:
        raise ValueError("online_seconds must be greater than 0")

    init_db(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
            """
            SELECT device_id,timestamp,status
            FROM sensor_data
            WHERE device_id = ?
            ORDER BY timestamp DESC, id DESC
            LIMIT 1
            """,
            (device_id,),
        )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None
    
    last_seen_text = row[1]
    device_status = row[2]

    try:
        last_seen = datetime.fromisoformat(last_seen_text)
        current_time = now or datetime.now()
        age_seconds = max(0, (current_time - last_seen).total_seconds())
        online_status = "online" if age_seconds <= online_seconds else "offline"
    except ValueError:
        age_seconds = None
        online_status = "unknown"

    return {
    "device_id": row[0],
    "last_seen": row[1],
    "device_status": row[2],
    "online_status": online_status,
    "age_seconds": age_seconds,
    }
